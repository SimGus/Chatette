#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
from random import seed as random_seed

from chatette import __version__
from chatette.adapters import JsonListAdapter
from chatette.adapters.rasa import RasaAdapter
from chatette.generator import Generator
from chatette.parsing.parser import Parser
from chatette.utils import print_DBG


def main():
    # pylint: disable=bad-continuation
    argument_parser = argparse.ArgumentParser(
        description="Chatette v"+__version__+" -- " +
                    "Generates NLU datasets from template files",
        epilog="SimGus -- 2018 -- Released under MIT license",
        prog="Chatette",
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
                                 help="Write adapter. Possible values: "+
                                      "['rasa', 'jsonl']")

    argument_parser.add_argument("-v", "--version", action="version",
                                 version="%(prog)s v"+__version__,
                                 help="Print the version number of the module")

    if len(sys.argv[1:]) == 0:
        argument_parser.print_help()
        argument_parser.exit()

    args = argument_parser.parse_args()

    facade = Facade.get_or_create_from_args(args)
    facade.run()


class Facade(object):
    """
    Facade of the whole program in charge of instantiating the different
    components required for the parsing, generation and writing of the
    relevant informations.
    Implements the design patterns facade and singleton.
    """
    instance = None
    def __init__(self, master_file_path, output_dir_path, adapter_str, local,
                 seed):
        self.master_file_path = master_file_path
        if local:
            self.output_dir_path = os.path.dirname(master_file_path)
        else:
            self.output_dir_path = os.getcwd()
        if output_dir_path is None:
            self.output_dir_path = os.path.join(self.output_dir_path, "output")
        else:
            self.output_dir_path = os.path.join(self.output_dir_path,
                                                output_dir_path)

        # Initialize the random number generator
        if seed is not None:
            random_seed(seed)

        if adapter_str is None:
            self.adapter = None
        elif adapter_str == "rasa":
            self.adapter = RasaAdapter()
        elif adapter_str == "jsonl":
            self.adapter = JsonListAdapter()
        else:
            raise ValueError("Unknown adapter was selected")

        self.parser = None
        self.generator = None
    @classmethod
    def from_args(cls, args):
        return cls(args.input, args.output, args.adapter, args.local, args.seed)

    @staticmethod
    def get_or_create(master_file_path, output_dir_path, adapter_str=None,
                      local=False, seed=None):
        if Facade.instance is None:
            instance = Facade(master_file_path, output_dir_path, adapter_str,
                              local, seed)
        return instance
    @staticmethod
    def get_or_create_from_args(args):
        if Facade.instance is None:
            instance = Facade.from_args(args)
        return instance

    def run(self):
        """
        Executes the parsing, generation and (if needed) writing of the output.
        """
        self.parser = Parser(self.master_file_path)
        self.parser.parse()

        self.generator = Generator(self.parser)
        synonyms = self.generator.get_entities_synonyms()

        train_examples = list(self.generator.generate_train())
        if train_examples:
            self.adapter.write(os.path.join(self.output_dir_path, "train"),
                               train_examples, synonyms)
        test_examples = list(self.generator.generate_test(train_examples))
        if test_examples:
            self.adapter.write(os.path.join(self.output_dir_path, "test"),
                               test_examples, synonyms)
        print_DBG("Generation over")


if __name__ == "__main__":
    main()
