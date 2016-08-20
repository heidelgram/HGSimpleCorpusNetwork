# Introduction
This tool can be used to do batch frequency analysis on unreliable corpus data. Given a set of search terms and a set of text files, the script will generate an adjacency matrix, a gexf file, and a graphml file linking the search terms to the texts.

![Functionality](documentation/functionality-I.png)

In order to account for unreliable data (i.e. ocr corrupted data), the search algorithm supports levenshtein distances and 
gestalt pattern matching in order to also recognize similar (i.e. distorted) tokens. For example, the algorithm is able to recognize _do1or_* as _dolor_. This enables fairly accurate frequency estimates, even when dealing with highly corrupted data.

# Requirements
* Python 2.x
* Python modules: networkx, numpy, nltk, matplotlib

# Usage
Run `runHGSCN.py` and supply the following arguments:

* -t Tokenizer (either 'simple' or 'nltk')
* -ma Matching Algorithm (either 'gestalt' or 'levenshtein')
* -mt Matching Threshold (n steps for levenshtein or 0-1 for gestalt)
* -pre Show Preview (either 1 or 0)
* file_dir (the corpus directory)
* project_name (a descriptive name for the batch)
* search\_terms\_file (a text file with one search term per line)

# Runtime
The script utilizes a simple linear search algorithm. Hence, the tool currently performs at O(n). The number of files is neglectable, what counts is the number of words and the number of search terms. Doubling the number of words will approximately double the runtime of the script. The same holds true for additional search terms.

# Known Flaws and Problems
* The script currently fails when it encounters malformed utf8 characters. Make sure that all corpus files are correctly encoded.