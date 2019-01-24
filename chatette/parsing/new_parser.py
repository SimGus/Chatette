"""
Module `chatette.parsing.new_parser`
Contains the (new) parser that reads and parses template files
and transforms the information they contain into dictionaries
of unit definitions.
"""

import os

from chatette.utils import print_DBG, print_warn
import chatette.parsing.parser_utils as pu
from chatette.parsing.tokenizer import Tokenizer

from chatette.units.word.rule_content import WordRuleContent
from chatette.units.word.group_rule_content import GroupWordRuleContent
from chatette.units.choice import ChoiceRuleContent
from chatette.units.alias import AliasDefinition, AliasRuleContent
from chatette.units.slot import SlotDefinition, \
                                SlotRuleContent, DummySlotValRuleContent
from chatette.units.intent import IntentDefinition, IntentRuleContent


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
        self.print_DBG()
    
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
        if self._currently_parsed_declaration is None:
            self.tokenizer.syntax_error("Got a rule outside of "+
                                        "a unit declaration.")

        self._check_indentation(tokens[0])

        # Remove alternative slot rule if necessary
        alt_slot_value = None  # TODO DummySlotVal absolutely need to be managed differently
        if self._currently_parsed_declaration[0] == pu.UnitType.slot:
            answer = pu.find_alt_slot_and_index(tokens)
            if answer is not None:
                (end_index, alt_slot_value) = answer
                tokens = tokens[:end_index]

        sub_rules = []
        leading_space = False
        for sub_rule_tokens in pu.next_sub_rule_tokens(tokens[1:]):
            if len(sub_rule_tokens) == 1 and sub_rule_tokens[0] == ' ':
                leading_space = True
                continue

            sub_rule = self._make_sub_rule_from_tokens(sub_rule_tokens,
                                                       leading_space)
            if alt_slot_value is not None:
                sub_rules = [DummySlotValRuleContent(alt_slot_value, sub_rule)]
                alt_slot_value = None
            sub_rules.append(sub_rule)
            
            leading_space = False

        relevant_dict = None
        if self._currently_parsed_declaration[0] == pu.UnitType.alias:
            relevant_dict = self.alias_definitions
        elif self._currently_parsed_declaration[0] == pu.UnitType.slot:
            relevant_dict = self.slot_definitions
        else:  # intent
            relevant_dict = self.intent_definitions
        
        name = self._currently_parsed_declaration[1]
        variation_name = self._currently_parsed_declaration[2].variation_name
        relevant_dict[name].add_rule(sub_rules, variation_name)

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

    def _make_sub_rule_from_tokens(self, sub_rule_tokens, leading_space):
        if pu.is_sub_rule_word(sub_rule_tokens):
            word_text = sub_rule_tokens[0]
            word = WordRuleContent(word_text, leading_space)
            return word
        elif pu.is_sub_rule_word_group(sub_rule_tokens):
            group_interior_tokens = sub_rule_tokens[1:-1]
            words = pu.find_words(group_interior_tokens)
            words_str = ''.join(words)
            modifiers = pu.find_modifiers_word_group(group_interior_tokens)
            # TODO check modifiers
            word_group = \
                GroupWordRuleContent(words_str, leading_space,
                                        casegen=modifiers.casegen,
                                        randgen=modifiers.randgen_name,
                                        percentage_gen=modifiers.percentage_randgen)
            return word_group
        elif pu.is_sub_rule_choice(sub_rule_tokens):
            choice_interior_tokens = sub_rule_tokens[1:-1]
            modifiers = pu.find_modifiers_choice(choice_interior_tokens)
            choice = ChoiceRuleContent(''.join(choice_interior_tokens),
                                        leading_space,
                                        casegen=modifiers.casegen,
                                        randgen=modifiers.randgen)#,
                                        #percentage_gen=modifiers.percentage_randgen)
            for choice_tokens in pu.next_choice_tokens(choice_interior_tokens):
                current_leading_space = False
                current_choice_sub_rules = []
                for choice_sub_rule_tokens in pu.next_sub_rule_tokens(choice_tokens):
                    if choice_sub_rule_tokens == ' ':
                        current_leading_space = True
                        continue
                    choice_sub_rule = \
                        self._make_sub_rule_from_tokens(choice_sub_rule_tokens,
                                                        current_leading_space)
                    current_choice_sub_rules.append(choice_sub_rule)
                    current_leading_space = False
                choice.add_choice(current_choice_sub_rules)
            return choice
        elif pu.is_sub_rule_alias_ref(sub_rule_tokens):
            alias_interior_tokens = sub_rule_tokens[2:-1]
            name = pu.find_name(alias_interior_tokens)
            modifiers = pu.find_modifiers_reference(alias_interior_tokens)
            # TODO check modifiers
            alias = AliasRuleContent(name, leading_space,
                                        modifiers.variation_name,
                                        modifiers.argument_value,
                                        modifiers.casegen,
                                        modifiers.randgen_name,
                                        modifiers.percentage_randgen, self)
            return alias
        elif pu.is_sub_rule_slot_ref(sub_rule_tokens):
            slot_interior_tokens = sub_rule_tokens[2:-1]
            name = pu.find_name(slot_interior_tokens)
            modifiers = pu.find_modifiers_reference(slot_interior_tokens)
            # TODO check modifiers
            slot = SlotRuleContent(name, leading_space,
                                    modifiers.variation_name,
                                    modifiers.argument_value,
                                    modifiers.casegen,
                                    modifiers.randgen_name,
                                    modifiers.percentage_randgen, self)
            return slot
        elif pu.is_sub_rule_intent_ref(sub_rule_tokens):
            intent_interior_tokens = sub_rule_tokens[2:-1]
            name = pu.find_name(intent_interior_tokens)
            modifiers = pu.find_modifiers_reference(intent_interior_tokens)
            # TODO check modifiers
            intent = IntentRuleContent(name, leading_space,
                                        modifiers.variation_name,
                                        modifiers.argument_value,
                                        modifiers.casegen,
                                        modifiers.randgen_name,
                                        modifiers.percentage_randgen, self)
            return intent
        else:
            self.tokenizer.syntax_error("Invalid type of sub-rule.",
                                        word_to_find=sub_rule_tokens[0])


    def print_DBG(self):
        print("Aliases:")
        for alias_name in self.alias_definitions:
            self.alias_definitions[alias_name].print_DBG()
        print("Slots:")
        for slot_name in self.slot_definitions:
            self.slot_definitions[slot_name].print_DBG()
        print("Intents:")
        for intent_name in self.intent_definitions:
            self.intent_definitions[intent_name].print_DBG()
        print()