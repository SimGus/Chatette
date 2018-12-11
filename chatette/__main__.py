#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import io
import os
import sys
from random import seed as random_seed

from chatette.adapters import JsonListAdapter
from chatette.adapters.rasa import RasaAdapter
from chatette.generator import Generator
from chatette.parsing import Parser
from chatette.utils import print_DBG


def main():
    argument_parser = argparse.ArgumentParser(
        description="Chatette v1.2.2 -- " +
                    "Generates NLU datasets from a template file",
        epilog="SimGus -- 2018 -- Released under MIT license",
        add_help=True)

    argument_parser.add_argument("input", type=str,
                                 help="Path to master template file")

    argument_parser.add_argument("-o", "--out", dest="output", required=False,
                                 type=str, default=None,
                                 help="Output directory path")

    argument_parser.add_argument("-s", "--seed", dest="seed", required=False,
                                 type=str, default=None,
                                 help="Seed for the random generator " +
                                      "(any string without spaces will work)")

    argument_parser.add_argument("-l", "--local", dest="local", required=False,
                                 action="store_true", default=False,
                                 help="Change the base directory for output " +
                                      "files from the current working directory " +
                                      "to the directory containing the template " +
                                      "file")

    argument_parser.add_argument("-a", "--adapter", dest="adapter", required=False,
                                 type=str, default="rasa",
                                 help="Write adapter. Possible values: ['rasa', 'jsonl']")

    if len(sys.argv[1:]) == 0:
        argument_parser.print_help()
        argument_parser.exit()

    args = argument_parser.parse_args()

    template_file_path = args.input
    if args.local:
        dir_path = os.path.dirname(template_file_path)
    else:
        dir_path = os.getcwd()

    dir_path = os.path.join(dir_path, "output")

    # Initialize the random number generator
    if args.seed is not None:
        random_seed(args.seed)

    with io.open(template_file_path, 'r') as in_file:
        parser = Parser(in_file)
        parser.parse()
        # parser.print_DBG()

    if args.adapter == 'rasa':
        adapter = RasaAdapter()
    elif args.adapter == 'jsonl':
        adapter = JsonListAdapter()
    else:
        raise ValueError("Unknown adapter was selected")

    generator = Generator(parser)
    synonyms = generator.get_entities_synonyms()

    train_examples = list(generator.generate_train())
    if train_examples:
        adapter.write(os.path.join(dir_path, "train"), train_examples, synonyms)

    test_examples = list(generator.generate_test(train_examples))
    if test_examples:
        adapter.write(os.path.join(dir_path, "test"), test_examples, synonyms)

    print_DBG("Generation over")


if __name__ == "__main__":
    main()
