"""
Module `chatette.facade`
Contains a facade to the system, allowing to run the parsing, generation and
writing of the output file(s).
"""

import os
from random import seed as random_seed

from chatette.utils import print_DBG
from chatette.parsing.parser import Parser
from chatette.generator import Generator
from chatette.adapters.rasa import RasaAdapter
from chatette.adapters.jsonl import JsonListAdapter


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

        self.parser = Parser(master_file_path)
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
    
    def run_parsing(self):
        """Executes the parsing alone."""
        self.parser.parse()
    
    def parse_file(self, filepath):
        """
        Parses the new template file at `filepath` with the current parser.
        """
        self.parser.open_new_master_file(filepath)
        self.parser.parse()
    

    def get_stats_as_str(self):
        if self.parser is None:
            return "\tNo file parsed."
        stats = self.parser.stats
        result = '\t' + str(stats["#files"]) + " files parsed\n" + \
                 '\t' + str(stats["#declarations"]) + " declarations: " + \
                 str(stats["#intents"]) + " intents, " + \
                 str(stats["#slots"]) + " slots and " + \
                 str(stats["#aliases"]) + " aliases\n" + \
                 '\t' + str(stats["#rules"]) + " rules"
        return result