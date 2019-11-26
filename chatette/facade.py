# coding: utf-8
"""
Module `chatette.facade`
Contains a facade to the system, allowing to run the parsing, generation and
writing of the output file(s).
"""

import os
import shutil
from random import seed as random_seed
from six.moves import input, getcwd

from chatette.utils import Singleton, print_DBG, print_warn, random_string
from chatette.parsing.parser import Parser
from chatette.generator import Generator
import chatette.adapters.factory as adapter_factory

from chatette.statistics import Stats
from chatette.deprecations import Deprecations
from chatette.units.ast import AST
from chatette.parsing.input_file_manager import InputFileManager


class Facade(Singleton):
    """
    Facade of the whole program in charge of instantiating the different
    components required for the parsing, generation and writing of the
    relevant informations.
    Implements the design patterns facade and singleton.
    """
    _instance = None
    def __init__(self,
        master_file_path, output_dir_path=None, adapter_str="rasa",
        base_filepath=None, local=False, seed=None, force_overwriting=False
    ):
        self.master_file_path = master_file_path
        if local:
            self.output_dir_path = os.path.dirname(master_file_path)
        else:
            self.output_dir_path = getcwd()
        if output_dir_path is None:
            self.output_dir_path = os.path.join(self.output_dir_path, "output")
        else:
            self.output_dir_path = os.path.join(self.output_dir_path,
                                                output_dir_path)

        self.force_overwriting = force_overwriting

        # Initialize the random number generator
        if seed is None:
            seed = random_string()
            print("Executing Chatette with random seed '" + seed + "'.")
        else:
            print("Executing Chatette with seed '" + seed + "'.")
        random_seed(seed)

        self.adapter = adapter_factory.create_adapter(
            adapter_str, base_filepath
        )

        self.parser = Parser()
        self.generator = None

    @classmethod
    def from_args(cls, args):
        return cls(
            args.input, args.output, args.adapter, args.base_filepath,
            args.local, args.seed, args.force
        )
    @classmethod
    def get_or_create_from_args(cls, args):
        if cls._instance is None:
            cls._instance = cls.from_args(args)
        return cls._instance


    @classmethod
    def reset_system(cls, *args, **kwargs):
        Stats.reset_instance()
        Deprecations.reset_instance()
        AST.reset_instance()
        InputFileManager.reset_instance(None)
        return cls.reset_instance(*args, **kwargs)


    def run(self):
        """
        Executes the parsing, generation and (if needed) writing of the output.
        """
        self.run_parsing()
        self.run_generation()

    def run_parsing(self):
        """Executes the parsing alone."""
        self.parser.parse_file(self.master_file_path)

    def parse_file(self, file_path):
        """
        Parses the new template file at `file_path` with the current parser.
        """
        self.parser.parse_file(file_path)

    def run_generation(self, adapter_str=None):
        """"
        Runs the generation of all intents and writes them out to the output
        file(s) using the adapter `adapter` if one is provided.
        @pre: the parsing has been done.
        """
        if adapter_str is None:
            adapter = self.adapter
        else:
            adapter = adapter_factory.create_adapter(adapter_str)

        self.generator = Generator()
        synonyms = AST.get_or_create().get_entities_synonyms()

        if os.path.exists(self.output_dir_path):
            if self.force_overwriting or self._ask_confirmation():
                shutil.rmtree(self.output_dir_path)
            else:
                print_DBG("Aborting generation. Exiting without any change.")
                return

        train_examples = list(self.generator.generate_train())
        if train_examples:
            adapter.write(os.path.join(self.output_dir_path, "train"),
                          train_examples, synonyms)
        test_examples = list(self.generator.generate_test(train_examples))
        if test_examples:
            adapter.write(os.path.join(self.output_dir_path, "test"),
                          test_examples, synonyms)
        print_DBG("Generation over")

    def _ask_confirmation(self):
        print_warn("Folder '" + self.output_dir_path + "' already exists.")
        answer = input("Overwrite the whole folder? [y/n] ").lower()
        print('')
        if answer == "" or answer.startswith('y'):
            return True
        return False


    def get_stats_as_str(self):
        stats = Stats.get_or_create()
        result = '\t' + str(stats.get_nb_files()) + " files parsed\n" + \
                 '\t' + str(stats.get_nb_declarations()) + " declarations: " + \
                 str(stats.get_nb_intents()) + " intents, " + \
                 str(stats.get_nb_slots()) + " slots and " + \
                 str(stats.get_nb_aliases()) + " aliases\n" + \
                 '\t' + str(stats.get_nb_rules()) + " rules"
        return result
