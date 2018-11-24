#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import io
import os
import sys
from random import seed as random_seed

try:
   from chatette.generator import Generator
   from chatette.parsing import Parser
except ImportError:
   from generator import Generator
   from parsing import Parser

DEFAULT_OUTPUT_FILENAME = "output.json"
DEFAULT_TESTING_DATASET_FILENAME = "testing-dataset.json"


def main():
    argument_parser = argparse.ArgumentParser(
        description= "Chatette v1.2.2 -- "+
                     "Generates Rasa NLU datasets from a template file",
        epilog="SimGus -- 2018 -- Released under MIT license",
        add_help=True)
    argument_parser.add_argument("input", type=str,
                                 help="Path to master template file")
    argument_parser.add_argument("-o", "--out", dest="output", required=False,
                                 type=str, default=None,
                                 help="Output file path")
    argument_parser.add_argument("-s", "--seed", dest="seed", required=False,
                                 type=str, default=None,
                                 help="Seed for the random generator "+
                                      "(any string without spaces will work)")
    argument_parser.add_argument("-l", "--local", dest="local", required=False,
                                 action="store_true", default=False,
                                 help="Change the base directory for output "+
                                      "files from the current working directory "+
                                      "to the directory containing the template "+
                                      "file")
    if len(sys.argv[1:]) == 0:
        argument_parser.print_help()
        argument_parser.exit()

    args = argument_parser.parse_args()

    template_file_path = args.input
    if args.local:
        dir_path = os.path.dirname(template_file_path)
    else:
        dir_path = os.getcwd()
    output_filename = DEFAULT_OUTPUT_FILENAME

    if args.output is not None:
        output_filename = args.output

    output_file_path = os.path.join(dir_path, output_filename)
    testing_filename = DEFAULT_TESTING_DATASET_FILENAME
    testing_file_path = os.path.join(dir_path, testing_filename)

    # Initialize the random number generator
    if args.seed is not None:
        random_seed(args.seed)

    with io.open(template_file_path, 'r') as in_file:
        parser = Parser(in_file)
        parser.parse()
        # parser.printDBG()
    print("")

    generator = Generator(output_file_path, testing_file_path, parser)
    generator.generate()


if __name__ == "__main__":
    main()
