import os

from chatette.utils import print_DBG, print_warn
import chatette.parsing.parser_utils as pu
from chatette.parsing.tokenizer import Tokenizer

from chatette.units.alias import AliasDefinition
from chatette.units.slot import SlotDefinition
from chatette.units.intent import IntentDefinition


class Parser(object):
    """
    **This class is a refactor of the current parser**
    This class will parse the input file(s)
    and create an internal representation of its contents.
    """
    
    def __init__(self, master_filename):
        self.tokenizer = Tokenizer(master_filename)
        
        self._expecting_rule = False
        self._currently_parsed_declaration = None  # 3-tuple
        self._expected_indentation = None  # str

        self.alias_definitions = dict()
        self.slot_definitions = dict()
        self.intent_definitions = dict()


    def parse(self):
        """
        Parses the master file and subsequent files and
        transforms the information parsed into a dictionary of 
        declaration names -> rules.
        """
        print_DBG("Parsing master file: "+self.tokenizer.get_file_information()[0])
        for token_line in self.tokenizer.next_tokenized_line():
            if not token_line[0].isspace():
                self._parse_declaration_initiator(token_line)
                self._expecting_rule = True
                self._expected_indentation = None
            else:
                self._parse_rule(token_line)
                self._expecting_rule = False  # Not expecting but still allowed
        self.tokenizer.close_files()

        # TEMP
        print("aliases:",self.alias_definitions)
        print("slots:",self.slot_definitions)
        print("intents:",self.intent_definitions)
    
    def _parse_declaration_initiator(self, token_line):
        """Parses a line (as tokens) that contains a declaration initiator."""
        if self._expecting_rule:
            self.tokenizer.syntax_error("Expected a generation rule, got a "+
                                        "unit declaration instead.")
        
        unit_type = pu.get_unit_type_from_sym(token_line[0])
        
        declaration_interior = pu.get_declaration_interior(token_line)
        if declaration_interior is None:
            self.tokenizer.syntax_error("Couldn't find a valid unit declaration.")

        try:
            pu.check_declaration_validity(declaration_interior)
        except SyntaxError as e:
            self.tokenizer.syntax_error(e.__str__())
        
        unit_name = pu.find_name(declaration_interior)
        modifiers = pu.find_modifiers_decl(declaration_interior)
        nb_examples_asked = None
        if unit_type == pu.UnitType.intent:
            annotation_interior = pu.get_annotation_interior(token_line)
            if annotation_interior is not None and len(annotation_interior) > 2:
                nb_examples_asked = pu.find_nb_examples_asked(annotation_interior)
        
        self.create_unit(unit_type, unit_name, modifiers, nb_examples_asked)
        self._currently_parsed_declaration = (unit_type, unit_name, modifiers)
    
    def create_unit(self, unit_type, unit_name, modifiers,
                    nb_examples_asked=None):
        """
        Creates a unit of type `unit_type` with name `unit_name` and modifiers
        `modifiers` inside the relevant dictionary (`alias_definitions`,
        `slot_definitions` or `intent_definitions`).
        `modifiers` is a `UnitDeclarationModifiersRepr` and `nb_examples_asked`
        is a tuple (training, test).
        """
        new_unit = None
        relevant_dict = None
        if unit_type == pu.UnitType.alias:
            new_unit = AliasDefinition(unit_name, [], modifiers.argument_name,
                                       modifiers.casegen)
            relevant_dict = self.alias_definitions
        elif unit_type == pu.UnitType.slot:
            new_unit = SlotDefinition(unit_name, [], modifiers.argument_name,
                                      modifiers.casegen)
            relevant_dict = self.slot_definitions
        elif unit_type == pu.UnitType.intent:
            new_unit = IntentDefinition(unit_name, [], modifiers.argument_name,
                                        modifiers.casegen)
            relevant_dict = self.intent_definitions

        if unit_type == pu.UnitType.intent and nb_examples_asked is not None:
            (train_nb, test_nb) = nb_examples_asked
            new_unit.set_nb_examples_asked(train_nb, test_nb)

        if unit_name not in relevant_dict:
            relevant_dict[unit_name] = new_unit
        else:  # Not allowed anymore
            self.tokenizer.syntax_error("The "+unit_type.name+" "+unit_name+
                                        " was declared several times.")


    def _parse_rule(self, tokens):
        """
        Parses the list of string `tokens` that represents a rule in a
        template file. Add the rule to the declaration currently being parsed.
        """
        # TODO check rule is valid
        print("PARSING RULE:",tokens)

        self._check_indentation(tokens[0])
        for sub_rule_tokens in pu.next_sub_rule_tokens(tokens[1:]):
            print(sub_rule_tokens)

    def _check_indentation(self, indentation):
        """
        Checks that the str `indentation` is the same
        as the expected indentation from the last parsed rule.
        Raises a `SyntaxError` if it isn't.
        """
        if self._expected_indentation is None:
            self._expected_indentation = indentation
            return
        if indentation != self._expected_indentation:
            self.tokenizer.syntax_error("Inconsistent indentation.")