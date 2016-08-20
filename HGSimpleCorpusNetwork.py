#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import defaultdict
from difflib import SequenceMatcher
from nltk.tokenize import word_tokenize
import networkx as nx
import os
import sys
import time
from HGDrawGraph import draw_graph
import numpy
import warnings

# noinspection PyCompatibility
reload(sys)
sys.setdefaultencoding('utf8')
warnings.simplefilter(action='ignore', category=RuntimeWarning)


def text_length(text, tokenizer):
    """Return the length of a given string.

    :param text: location of a .txt file
    :type text: string
    :param tokenizer: the tokenizer that should be used (nltk or simple)
    :type tokenizer: string
    :return: number of tokens
    :rtype: int
    """
    text = open(text, 'r')
    if tokenizer == 'nltk':
        return len(word_tokenize(text.read()))
    elif tokenizer == 'simple':
        tokens = 0
        for line in text:
            for word in line.split():
                tokens += 1
        return tokens


def lines_in_file(file):
    """Return the number of lines in a given text file.

    :param file: location of a .txt file
    :type file: string
    :return: number of lines the the file
    :rtype: int
    """
    with open(file) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def levenshtein(a, b):
    """Calculate the levenhstein distance between two strings.

    :param a: first word
    :type a: string
    :param b: second word
    :type b: string
    :return: levenshtein distance between a and b
    :rtype: int
    """
    if len(a) < len(b):
        return levenshtein(b, a)

    if len(b) == 0:
        return len(a)

    previous_row = range(len(b) + 1)
    for i, c1 in enumerate(a):
        current_row = [i + 1]
        for j, c2 in enumerate(b):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def write_finding(search_term, text, concordance, match_algorithm, confidence, project_name):
    """Write the findings to a csv file.

    :param search_term: the word to look for
    :type search_term: string
    :param text: location of a .txt file
    :type text: string
    :param concordance: a concordance string
    :type concordance: string
    :param match_algorithm: the matching algorithm
    :type match_algorithm: string
    :param confidence: the confidence
    :type confidence: float
    :param project_name: the project's name
    :type project_name: string
    :return: none
    """
    if not os.path.isfile('output/' + project_name + '/findings.csv'):
        with open('output/' + project_name + '/findings.csv', 'a') as findings_file:
            findings_file.write('search_term;search_file;match_algorithm;confidence;concordance;project_name\n')

    with open('output/' + project_name + '/findings.csv', 'a') as findings_file:
        findings_file.write(
            search_term + ';' + text.name + ';' + match_algorithm + ';' + str(confidence) + ';' + concordance.replace(
                ';', ',') + ';' + project_name + '\n')


def search_word_count(search_term, text, match_threshold, match_algorithm, project_name):
    """Return a dictionary wwith the number of findings and a confidence using the simple tokenizer.

    :param search_term: the word to look for
    :type search_term: string
    :param text: a file object pointing to a .txt file
    :type text: file
    :param match_threshold: the matching threshold
    :type match_algorithm: float
    :param match_algorithm: the matching algorithm
    :type match_algorithm: string
    :param project_name: the project's name
    :type project_name: string
    :return: dictionary containing the instances and the average_confidence
    :rtype: dict
    """
    instances = 0
    confidence = []
    for line in text:
        for word in line.split():
            if match_algorithm == 'gestalt':
                if SequenceMatcher(None, search_term, word).ratio() >= match_threshold:
                    confidence.append(SequenceMatcher(None, search_term, word).ratio())
                    instances += 1
                    write_finding(search_term, text, line.rstrip(), match_algorithm,
                                  SequenceMatcher(None, search_term, word).ratio(),
                                  project_name)
            else:
                if levenshtein(search_term, word) <= match_threshold:
                    confidence.append(levenshtein(search_term, word))
                    instances += 1
                    write_finding(search_term, text, line.rstrip(), match_algorithm, levenshtein(search_term, word),
                                  project_name)

    if round(numpy.mean(numpy.fromiter(iter(confidence), dtype=float)), 2) > 0:
        average_confidence = round(numpy.mean(numpy.fromiter(iter(confidence), dtype=float)), 2)
    else:
        average_confidence = 0

    return {'instances': instances, 'average_confidence': average_confidence}


def search_word_count_nltk(search_term, text, match_threshold, match_algorithm, project_name):
    """Return a dictionary wwith the number of findings and a confidence using the nltk tokenizer.

    :param search_term: the word to look for
    :type search_term: string
    :param text: a file object pointing to a .txt file
    :type text: file
    :param match_threshold: the matching threshold
    :type match_algorithm: float
    :param match_algorithm: the matching algorithm
    :type match_algorithm: string
    :param project_name: the project's name
    :type project_name: string
    :return: dictionary containing the instances and the average_confidence
    :rtype: dict
    """
    instances = 0
    confidence = []
    current_word = 0
    words = word_tokenize(text.read())

    for word in words:
        # Calculate Concordance
        concordance = ''
        for x in range(-7, 7):
            try:
                concordance = concordance + words[current_word + x] + ' '
            except:
                pass
        current_word += 1

        if match_algorithm == 'gestalt':
            if SequenceMatcher(None, search_term, word).ratio() >= match_threshold:
                confidence.append(SequenceMatcher(None, search_term, word).ratio())
                instances += 1
                write_finding(search_term, text, concordance.rstrip(), match_algorithm,
                              SequenceMatcher(None, search_term, word).ratio(),
                              project_name)
        else:
            if levenshtein(search_term, word) <= match_threshold:
                confidence.append(levenshtein(search_term, word))
                instances += 1
                write_finding(search_term, text, concordance.rstrip(), match_algorithm, levenshtein(search_term, word),
                              project_name)

    if round(numpy.mean(numpy.fromiter(iter(confidence), dtype=float)), 2) > 0:
        average_confidence = round(numpy.mean(numpy.fromiter(iter(confidence), dtype=float)), 2)
    else:
        average_confidence = 0

    return {'instances': instances, 'average_confidence': average_confidence}


def generate(file_dir, project_name, search_terms_file, tokenizer, match_algorithm, match_threshold, show_preview):
    """Initate the search process.

    :param file_dir: the location of a directory with .txt files
    :type file_dir: string
    :param project_name: the project's name
    :type project_name: string
    :param search_terms_file: location to a .txt file containing search terms
    :type search_terms_file: string
    :param tokenizer: the tokenizer that should be used (nltk or simple)
    :type tokenizer: string
    :param match_algorithm: the matching algorithm
    :type match_algorithm: string
    :param match_threshold: the matching threshold
    :type match_threshold: float
    :param show_preview:  a boolean indicating if a preview should be shown to the user
    :type show_preview: int
    :note: Goes through the search terms and files one by one, calculating the occurrences
    :return: none
    """
    global max_count, search_term
    max_count = 0

    def search_in_files(search_term, tokenizer, match_algorithm, project_name):
        """Search a specific search term given a tokenizer and a matching algorithm.

        :param search_term: the word to look for
        :type search_term: string
        :param tokenizer: the tokenizer that should be used (nltk or simple)
        :type tokenizer: string
        :param match_algorithm: the matching algorithm
        :type match_algorithm: string
        :param project_name: the project's name
        :type project_name: string
        :return: none
        """
        global max_count
        for text in text_files:  # Loop through files
            f = open(file_dir + text, 'r')
            if tokenizer == 'simple':
                search_result = search_word_count(search_term, f, match_threshold, match_algorithm, project_name)
            else:
                search_result = search_word_count_nltk(search_term, f, match_threshold, match_algorithm, project_name)
            search_results[search_term][text] = search_result["instances"]

            f.close()

            # Adding nodes and edges to NetworkX object g
            if search_result['instances'] > 0:
                g.add_node(text.replace('.txt', ''), node_type='text', tokens=text_length(file_dir + text, tokenizer))
                g.add_node(search_term, node_type='search_term', tokens=0)
                g.add_edge(text.replace('.txt', ''), search_term, weight=search_result['instances'],
                           average_confidence=float(search_result['average_confidence']),
                           match_algorithm=match_algorithm)

            # Incrementing max_count if necessary
            if search_result['instances'] > max_count:
                max_count = search_result['instances']

    file_dir = os.path.join(file_dir, '')  # add trailing slash to the file_dir
    if os.path.isdir(file_dir):
        print('Running in: "' + file_dir + '" with search terms from "' + search_terms_file + '"')
    else:
        print('Not a valid folder!')
        exit()

    # Generate the graph object for NetworkX
    g = nx.DiGraph()

    if not os.path.exists('output/' + project_name):
        os.makedirs('output/' + project_name)

    text_files = os.listdir(file_dir)
    search_terms = open(search_terms_file, 'r')
    search_results = defaultdict(lambda: defaultdict(dict))  # Create Array search_results[search_term][search_text]
    csv_file = open('output/' + project_name + '/adjacencyMatrix.csv', 'w')
    no_search_terms = lines_in_file(search_terms_file)
    no_text_files = len(text_files)
    running_times = []
    search_term_counter = 0

    print('Matching Algorithm: ' + match_algorithm)
    print('Matching Threshold: ' + str(match_threshold))
    print('Tokenizer: ' + str(tokenizer))
    print('Show Preview: ' + str(show_preview))
    print('Project: ' + str(no_search_terms) + ' search terms and ' + str(no_text_files) + ' text files')

    # Loop through the individual search terms
    start_time_total = time.time()
    print('Processing first search term, please wait for an estimated running time...')

    for search_term in search_terms:
        start_time_term = time.time()
        search_term_counter += 1
        search_term = search_term.rstrip()
        search_in_files(search_term, tokenizer, match_algorithm, project_name)
        running_times.append(time.time() - start_time_term)
        estimated_time_left = round(numpy.mean(
            numpy.fromiter(iter(running_times), dtype=float) * (no_search_terms - search_term_counter) / 60), 1)
        print('Search Term ' + str(search_term_counter) + '/' + str(no_search_terms) + ' [Estimated time left: ' + str(
            estimated_time_left) + ' min]', end='\r')

    search_terms.close()
    print('\n\nTotal run-time: ' + str(round((time.time() - start_time_total) / 60, 3)) + ' minutes')

    # CSV Adjacency-Matrix Output
    csv_heading = 'Author'
    for text in search_results[search_term]:  # This must be a valid search_term.
        csv_heading = csv_heading + ';' + text.replace('.txt', '')
    csv_file.write(csv_heading + '\n')

    for search_term in search_results:
        csv_line = search_term
        for text in search_results[search_term]:
            csv_line = csv_line + ';' + str(search_results[search_term][text])
        csv_file.write(csv_line + '\n')
    csv_file.close()

    # NetworkX Output and Network Preview
    nx.write_gexf(g, 'output/' + project_name + '/network.gexf')
    nx.write_graphml(g, 'output/' + project_name + '/network.graphml')
    draw_graph(max_count, project_name, g, show_preview)
