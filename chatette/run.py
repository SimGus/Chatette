#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import io
import os
import sys

from chatette.generator import Generator
from chatette.parser import Parser

DEFAULT_OUTPUT_FILENAME = "output.json"
DEFAULT_TESTING_DATASET_FILENAME = "testing-dataset.json"


def main():
    argument_parser = argparse.ArgumentParser(
        description="Generates Rasa NLU datasets from a template file",
        add_help=True)
    argument_parser.add_argument("input", help="Path to template file",
                                 type=str)
    argument_parser.add_argument("-o", "--out", dest="output", required=False,
                                 help="Output file path",
                                 type=str, default=None)
    if len(sys.argv[1:]) == 0:
        argument_parser.print_help()
        argument_parser.exit()

    args = argument_parser.parse_args()

    template_file_path = args.input
    dir_path = os.path.dirname(template_file_path)
    output_filename = DEFAULT_OUTPUT_FILENAME

    if args.output:
        output_filename = args.output

    output_file_path = os.path.join(dir_path, output_filename)
    testing_filename = DEFAULT_TESTING_DATASET_FILENAME
    testing_file_path = os.path.join(dir_path, testing_filename)

    with io.open(template_file_path, 'r') as in_file:
        parser = Parser(in_file)
        parser.parse()
        # parser.printDBG()
    print("")

    generator = Generator(output_file_path, testing_file_path, parser)
    generator.generate()


if __name__ == "__main__":
    main()
