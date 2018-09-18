#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, io
from chatette.parser import Parser, Unit
from chatette.generator import Generator

DEFAULT_OUTPUT_FILENAME = "output.json"
DEFAULT_TESTING_DATASET_FILENAME = "testing-dataset.json"


def print_usage():
    print("This program generates Rasa NLU datasets from a template file.")
    print("Usage:\n\t'python3 run.py <TEMPLATE_FILE_PATH> [OUTPUT_FILE_PATH]' or")
    print("\t'./run.py <TEMPLATE_FILE_PATH> [OUTPUT_FILE_PATH]'")


if __name__ == "__main__":
    if len(sys.argv) <= 1 or len(sys.argv) > 3:
        print_usage()
    else:
        template_file_path = sys.argv[1]
        dir_path = os.path.dirname(template_file_path)
        output_filename = DEFAULT_OUTPUT_FILENAME
        if len(sys.argv) == 3:
            output_filename = sys.argv[2]
        output_file_path = os.path.join(dir_path, output_filename)
        testing_filename = DEFAULT_TESTING_DATASET_FILENAME
        testing_file_path = os.path.join(dir_path, testing_filename)

        parser = None
        with io.open(template_file_path, 'r') as in_file:
            parser = Parser(in_file)
            parser.parse()
            # parser.printDBG()
        print("")

        generator = Generator(output_file_path, testing_file_path, parser)
        generator.generate()
