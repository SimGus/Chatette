"""
Test module.
Tests the whole system as a black box.
"""

import os
import io, shutil

import pytest

from chatette.parsing import Parser
from chatette.generator import Generator
from chatette.adapters import RasaAdapter, JsonListAdapter


class ChatetteFacade(object):
    """
    A facade to the different objects and calls to their methods required to
    make the system perform a parsing, generation and output writing.
    This class is also a singleton.
    """
    instance = None
    def __init__(self):
        self.rasa_adapter = RasaAdapter()
        self.jsonl_adapter = JsonListAdapter

        self.cwd = os.getcwd()
        self.output_dirpath = \
            os.path.join(self.cwd, "tests/system-testing/output")

        self.generator = None
        self.train_examples = None
        self.test_examples = None

    @staticmethod
    def get_or_create():
        if ChatetteFacade.instance is None:
            ChatetteFacade.instance = ChatetteFacade()
        return ChatetteFacade.instance

    def run(self, template_filepath):
        with io.open(template_filepath, 'r') as in_file:
            parser = Parser(in_file)
            parser.parse()

        self.generator = Generator(parser)
        self.train_examples = list(self.generator.generate_train())
        self.test_examples = list(self.generator.generate_test())

    def write(self, adapter="rasa"):
        if self.generator is None:
            raise ValueError("Tried to write an output file before generation")
        if adapter == "rasa":
            adapter = self.rasa_adapter
        elif adapter == "jsonl":
            adapter = self.jsonl_adapter
        else:
            raise ValueError(adapter+" is not a valid adapter.")

        synonyms = self.generator.get_entities_synonyms()

        if self.train_examples:
            adapter.write(os.path.join(self.output_dirpath, "train"), 
                          self.train_examples, synonyms)
        
        if self.test_examples:
            adapter.write(os.path.join(self.output_dirpath, "train"),
                          self.test_examples, synonyms)

    def clean(self):
        shutil.rmtree(self.output_dirpath)


class TestSystem(object):
    solution_file_extension = ".solution"
    syn_solution_file_extension = ".syn"
    solution_marker = ">>>"

    @staticmethod
    def get_solution_filepath(input_filepath):
        """
        Returns the same file path as `input_filepath`
        with a different extension.
        """
        return os.path.splitext(input_filepath)[0] + \
               TestSystem.solution_file_extension

    @staticmethod
    def get_synonym_solution_filepath(input_filepath):
        """
        Returns the same file path as `input_filepath`
        with a different extension.
        """
        return os.path.splitext(input_filepath)[0] + \
               TestSystem.syn_solution_file_extension

    @staticmethod
    def get_legal_examples(input_filepath):
        """Returns the list of all legal examples for file `input_filepath`."""
        solution_filepath = TestSystem.get_solution_filepath(input_filepath)
        with io.open(solution_filepath, 'r') as f:
            solution_examples = f.readlines()
        return [{"intent": ex.split(TestSystem.solution_marker)[0],
                 "text": ex.split(TestSystem.solution_marker)[1].rstrip()}
                for ex in solution_examples
                if (not ex.startswith('#') and not ex.isspace())]

    @staticmethod
    def get_legal_synonyms(input_filepath):
        """
        Returns a dict with all legal synonyms
        or `None` if there is no synonym solution file.
        """
        syn_filepath = TestSystem.get_synonym_solution_filepath(input_filepath)
        if not os.path.isfile(syn_filepath):
            return None
        with io.open(syn_filepath, 'r') as f:
            result = dict()
            for l in f:
                if not l.startswith('#'):
                    [name, val] = l.rstrip().split("===")
                    if name not in result:
                        result[name] = [val]
                    else:
                        result[name].append(val)

        return result

    
    @staticmethod
    def check_no_duplicates(examples):
        """Returns `True` if there are no duplicates in the list"""
        return len(examples) == len(set(examples))


    def test_generate_all_training(self):
        """
        Tests templates that generate all possible examples for each intent
        and that generate only training data.
        """
        facade = ChatetteFacade.get_or_create()

        input_dir_path = "tests/system-testing/inputs/generate-all/"
        input_filenames = \
            ["simplest.chatette", "only-words.chatette",
             "words-and-groups.chatette", "alias.chatette", "include.chatette",
             "slot.chatette"]
        for filename in input_filenames:
            file_path = os.path.join(input_dir_path, filename)
            facade.run(file_path)
            if not TestSystem.check_no_duplicates(facade.train_examples):
                pytest.fail("Some examples were generated several times "+
                            "when dealing with file '"+filename+"'.\n"+
                            "Generated: "+str(facade.train_examples))
            legal_examples = TestSystem.get_legal_examples(file_path)
            for ex in facade.train_examples:
                formatted_ex = {"intent": ex.name, "text": ex.text}
                if formatted_ex not in legal_examples:
                    pytest.fail(str(formatted_ex) + 
                                " is not a legal example for '" +
                                file_path + "'")
            if len(legal_examples) != len(facade.train_examples):
                training_texts = [ex.text for ex in facade.train_examples]
                for legal_ex in legal_examples:
                    if legal_ex["text"] not in training_texts:
                        pytest.fail("Example '" + legal_ex["text"] + 
                                    "' was not generated.")
                pytest.fail("An unknown example was not generated (" + 
                            str(len(facade.train_examples)) + 
                            " generated instead of " +
                            str(len(legal_examples)) + ").\nGenerated: " +
                            str(facade.train_examples))
            legal_syn = TestSystem.get_legal_synonyms(file_path)
            if legal_syn is not None:
                synonyms = facade.generator.get_entities_synonyms()
                for key in synonyms:
                    if key not in legal_syn:
                        pytest.fail("'" + key +
                                    "' shouldn't have any synonyms.")
                    for syn in synonyms[key]:
                        if syn not in legal_syn[key]:
                            pytest.fail("'" + syn +
                                        "' shouldn't be a synonym of '" + 
                                        key + "'")

    def test_generate_all_testing(self):
        """
        Tests templates that generate all possible examples for each intent
        and that generate only testing data.
        NOTE: impossible (should it be permitted?)
        """
        pass

    def test_generate_nb_training(self):
        """
        Tests templates that generate a subset of all possible examples
        for each intent and that generate only training data.
        """
        facade = ChatetteFacade.get_or_create()

        input_dir_path = "tests/system-testing/inputs/generate-nb/training-only/"
        input_filenames = \
            ["only-words.chatette", "words-and-groups.chatette",
             "alias.chatette", "include.chatette", "slot.chatette"]
        for filename in input_filenames:
            file_path = os.path.join(input_dir_path, filename)
            facade.run(file_path)
            # if not TestSystem.check_no_duplicates(facade.train_examples):  # TODO: make sure there are no duplicates in this case
            #     pytest.fail("Some examples were generated several times "+
            #                 "when dealing with file '"+filename+"'.\n"+
            #                 "Generated: "+str(facade.train_examples))
            legal_examples = TestSystem.get_legal_examples(file_path)
            for ex in facade.train_examples:
                formatted_ex = {"intent": ex.name, "text": ex.text}
                if formatted_ex not in legal_examples:
                    pytest.fail(str(formatted_ex) + 
                                " is not a legal example for '" +
                                file_path + "'")
            
            legal_syn = TestSystem.get_legal_synonyms(file_path)
            if legal_syn is not None:
                synonyms = facade.generator.get_entities_synonyms()
                for key in synonyms:
                    if key not in legal_syn:
                        pytest.fail("'" + key +
                                    "' shouldn't have any synonyms.")
                    for syn in synonyms[key]:
                        if syn not in legal_syn[key]:
                            pytest.fail("'" + syn +
                                        "' shouldn't be a synonym of '" + 
                                        key + "'")

        filename_zero = "zero-ex.chatette"
        file_path = os.path.join(input_dir_path, filename_zero)
        facade.run(file_path)
        if len(facade.train_examples) != 0:
            pytest.fail("When dealing with file 'zero-ex.chatette', no "+
                        "examples should be generated.\nGenerated: "+
                        str(facade.train_examples))

        filename_one = "one-ex.chatette"
        file_path = os.path.join(input_dir_path, filename_one)
        facade.run(file_path)
        if len(facade.train_examples) != 1:
            pytest.fail("When dealing with file 'one-ex.chatette', one "+
                        "examples should be generated.\nGenerated: "+
                        str(facade.train_examples))

    def test_generate_nb_testing(self):
        """
        Tests templates that generate a subset of all possible examples
        for each intent and that generate only testing data.
        """
        pass

    def test_generate_nb(self):
        """
        Tests templates that generate a subset of all possible examples
        for each intent and that generate both training and testing data.
        """
        pass