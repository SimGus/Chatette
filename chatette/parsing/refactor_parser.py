"""
Module `chatette.parsing.refactor_parser`
Contains the (newest) parser that reads and parses template files
and transforms the information they contain into dictionaries
of unit definitions.
"""

from six import string_types

from chatette.utis import print_DBG, print_warn
import chatette.parsing_utils as pu

from chatette.parsing.tokenizer import Tokenizer
from chatette.units.ast import AST

from chatette.refactor_units.definitions.alias import Alias
from chatette.refactor_units.definitions.slots import Slot
from chatette.refactor_units.definitions.intent import Intent


class Parser(object):
    """
    This class will parse the input file(s)
    and creates an Abstract Syntax Tree (AST) representing their contents.
    """
    def __init__(self, master_filename):
        if not isinstance(master_filename, string_types):
            raise ValueError(
                "Since v1.4.0, the parser takes the path of the master file " + \
                "as an argument directly, rather than the file itself."
            )
        self.tokenizer = Tokenizer(master_filename)

        self._declaration_line_allowed = True
        self._currently_parsed_declaration = None  # 3-tuple
        self._expected_indentation = None  # str

        self.ast = AST.get_or_create(master_filename)
    

    def parse(self):
        """
        Parses the master file and subsequent files and
        transforms the information parsed into dictionaries of declarations.
        """
        print_DBG("Parsing master file: " + \
            self.tokenizer.get_current_file_name())
        
        for token_line in self.tokenizer.next_tokenized_line():
            if not pu.is_rule_line(token_line):
                if pu.is_include_line(token_line):
                    if self.ast.stats.new_file(tokn_line[1]):
                        self.tokenizer.open_file(token_line[1])
                        print_DBG("Parsing file: " + \
                            self.tokenizer.get_current_file_name())
                    else:
                        print_warn(
                            "Tried to parse file '" + token_line[1] + \
                            "' a second time while parsing '" + \
                            self.tokenizer.get_current_file_name() + \
                            "'. There might be circular includes in " + \
                            "the input files."
                        )
                else:
                    self.ast.stats.increment_declarations()
                    self._declaration_line_allowed = False
                    self._parse_declaration_initiator(token_line)
                self._expected_indentation = None
            else:
                self.ast.stats.increment_rules()
                self._declaration_line_allowed = True
                self._parse_rule(token_line)
        
        self.tokenizer.close_files()
        print_DBG("Parsing finished!")

        return self.ast
    
    def _parse_declaration_initiator(self, token_line):
        """
        Parses a line (as str tokens)
        that makes up the initiator of a declaration.
        """
        if not self._declaration_line_allowed:
            self.tokenizer.syntax_error(
                "Expected a generation rule, got a unit declaration instead."
            )
        
        unit_type = pu.get_unit_type_from_sym(token_line[0])
        declaration_interior = pu.get_declaration_interior(token_line)
        if declaration_interior is None:
            self.tokenizer.syntax_error(
                "Couldn't find a valid unit declaration."
            )

        try:
            pu.check_declaration_validity(declaration_interior)
        except SyntaxError as e:
            self.tokenizer.syntax_error(str(e))
        
        unit_name = pu.find_name(declaration_interior)
        modifiers = pu.find_modifiers_decl(declaration_interior)
        if unit_type == pu.UnitType.intent:
            nb_examples_asked = pu.get_nb_examples_asked(token_line)

        self.create_unit(unit_type, unit_name, modifiers, nb_examples_asked)
        self._currently_parsed_declaration = (unit_type, unit_name, modifiers)
    
    def create_unit(
        self, unit_type, unit_name, modifiers, nb_examples_asked=None
    ):
        """
        Creates a unit of type `unit_type` with name `unit_name` and modifers
        `modifiers` inside the AST.
        `modifiers` is a `UnitDeclarationModifiersRepr` and `nb_examples_asked`
        is a tuple (training, test).
        """
        # NOTE this if-else statement is also done in the function it calls
        if unit_type == pu.UnitType.alias:
            new_unit = Alias(unit_name)
            self.ast.stats.increment_aliases()
        elif unit_type == pu.UnitType.slot:
            new_unit = Slot(unit_name)
            self.ast.stats.increment_slots()
        elif unit_type == pu.UnitType.intent:
            new_unit = Intent(unit_name)
            self.ast.stats.increment_intents()
            if nb_examples_asked is not None:
                (train_nb, test_nb) = nb_examples_asked
                new_unit.set_nb_examples.asked(train_nb, test_nb)
        
        try:
            self.ast.add_unit(unit_type, unit_name, new_unit)
        except ValueError:  # NOTE can be a new variation
            pass
        