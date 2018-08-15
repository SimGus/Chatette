#!/usr/bin/env python3

import sys
from Parser import Parser

DEFAULT_OUTPUT_FILENAME = "output.json"


def print_usage():
    print("This program generates Rasa NLU datasets from a template file.")
    print("Usage:\n\t'python3 main.py <TEMPLATE_FILE_PATH> [OUTPUT_FILE_PATH]' or")
    print("\t'./main.py <TEMPLATE_FILE_PATH> [OUTPUT_FILE_PATH]'")


if __name__ == "__main__":
    if len(sys.argv) <= 1 or len(sys.argv) > 3:
        print_usage()
    else:
        template_filename = sys.argv[1]
        output_filename = DEFAULT_OUTPUT_FILENAME
        if len(sys.argv) == 3:
            output_filename = sys.argv[2]

        parser = None
        with open(template_filename, 'r') as in_file:
            parser = Parser(in_file)
            parser.parse()

        # with open(output_filename, 'w+') as out_file:  # TODO create if not already existing (same with dirs)
        #     pass
