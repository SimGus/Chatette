#!/usr/bin/env python3

import sys, os, io
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
        template_file_path = sys.argv[1]
        output_filename = DEFAULT_OUTPUT_FILENAME
        if len(sys.argv) == 3:
            output_filename = sys.argv[2]
        output_file_path = os.path.join(os.path.dirname(template_file_path), output_filename)

        parser = None
        with open(template_file_path, 'r') as in_file:
            parser = Parser(in_file)
            parser.parse()
            parser.printDBG()
        print("")

        with io.open(output_file_path, 'w+', encoding="utf-8") as out_file:  # TODO create if not already existing (same with dirs)
            generator = Generator(out_file, parser)
            generator.generate()
