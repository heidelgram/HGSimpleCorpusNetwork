import HGSimpleCorpusNetwork as scn
import sys
import argparse


def main():
    """Iniate the script.

    :return: returns nothing, but starts the program
    :note: initializes the program and takes the user's input.
    """
    print 'Author-Network-Analysis HGSimpleCorpusNetwork (01.11.2017)\nIngo Kleiber <kleiber@heiedu.uni-heidelberg.de>\n'
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('file_dir', help='The corpus directory containing .txt files', default='corpus/')
    parser.add_argument('project_name', help='The name of the current project.', default='network')
    parser.add_argument('search_terms_file',
                        help='A .txt file with the search terms. Each line should represent one term.',
                        default='searchTerms.txt')

    parser.add_argument('-t', '--tokenizer', type=str, nargs='*',
                        help='Specify the tokenizer used by the program. Either simple or nltk.', default='nltk')
    parser.add_argument('-ma', '--match_algorithm',
                        help='Specify the matching algorithm used by the program. Either gestalt or levenshtein.',
                        type=str,
                        default='gestalt')
    parser.add_argument('-mt', '--match_threshold', help='Specify the matching threshold used by the program.',
                        type=float, default=1.0)
    parser.add_argument('-pre', '--show_preview', help='Show a preview of the network.',
                        type=int, default=0)
    parser.add_argument('-icase', '--ignore_case', help='Ignore case.',
                        type=int, default=0)

    args = parser.parse_args()

    try:
        scn.generate(args.file_dir, args.project_name, args.search_terms_file, args.tokenizer[0],
                     args.match_algorithm, args.match_threshold, args.show_preview, args.ignore_case)
    except KeyboardInterrupt:
        print 'Stopping'
    except KeyError:
        pass
    except:
        print "\nUnexpected error:", sys.exc_info()
    finally:
        sys.exit()

if __name__ == '__main__':
    main()
