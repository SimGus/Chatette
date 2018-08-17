#!/usr/bin/env python3

import sys, io
from Parser import Parser, Unit
from Generator import Generator

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
            parser.printDBG()
        print("")

        with io.open(output_filename, 'w+', encoding="utf-8") as out_file:  # TODO create if not already existing (same with dirs)
            generator = Generator(out_file, parser)
            generator.generate()
