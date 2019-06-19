"""
Module `chatette.parsing.new_parser`
Contains the (new) parser that reads and parses template files
and transforms the information they contain into dictionaries
of unit definitions.
"""

from six import string_types

from chatette.utils import print_DBG, print_warn
import chatette.parsing.parser_utils as pu
from chatette.parsing.tokenizer import Tokenizer
from chatette.parsing.statistics import Stats

from chatette.units.ast import AST
from chatette.units.word.rule_content import WordRuleContent
from chatette.units.word.group_rule_content import GroupWordRuleContent
from chatette.units.choice import ChoiceRuleContent
from chatette.units.alias import AliasDefinition, AliasRuleContent
from chatette.units.slot import SlotDefinition, \
                                SlotRuleContent, DummySlotValRuleContent
from chatette.units.intent import IntentDefinition, IntentRuleContent


class Parser(object):
    """
    This class will parse the input file(s)
    and create an internal representation of its contents.
    """

    def __init__(self, master_filename):
        if not isinstance(master_filename, string_types):
            raise ValueError("Since v1.4.0, the parser takes as an argument " + \
                             "the path of the master file directly, rather " + \
                             "than the file itself as before.")
        self.tokenizer = Tokenizer(master_filename)

        self._declaration_line_allowed = True
        self._currently_parsed_declaration = None  # 3-tuple
        self._expected_indentation = None  # str

        self.ast = AST(master_filename)


    def open_new_master_file(self, master_filepath):
        self.tokenizer.redefine_master_file(master_filepath)
        self.ast.stats.new_file(master_filepath)


    def parse(self):
        """
        Parses the master file and subsequent files and
        transforms the information parsed into a dictionary of
        declaration names -> rules.
        """
        print_DBG("Parsing master file: " + self.tokenizer.get_current_file_name())

        for token_line in self.tokenizer.next_tokenized_line():
            if not pu.is_rule_line(token_line):
                if pu.is_include_line(token_line):
                    if self.ast.stats.new_file(token_line[1]):
                        self.tokenizer.open_file(token_line[1])
                        print_DBG("Parsing file: " + \
                                  self.tokenizer.get_current_file_name())
                    else:
                        print_warn("Tried to parse file '" + token_line[1] + \
                                   "' a second time while parsing '" + \
                                   self.tokenizer.get_current_file_name() + \
                                   "'. There might be circular " + \
                                   "includes in the input files.")
                else:
                    self._parse_declaration_initiator(token_line)
                    self._declaration_line_allowed = False
                    self.ast.stats.increment_declarations()
                self._expected_indentation = None
            else:
                self._parse_rule(token_line)
                self._declaration_line_allowed = True
                self.ast.stats.increment_rules()

        self.tokenizer.close_files()
        print_DBG("Parsing finished!")

        return self.ast

    def _parse_declaration_initiator(self, token_line):
        """Parses a line (as tokens) that contains a declaration initiator."""
        if not self._declaration_line_allowed:
            self.tokenizer.syntax_error("Expected a generation rule, got a "+
                                        "unit declaration instead.")

        unit_type = pu.get_unit_type_from_sym(token_line[0])

        declaration_interior = pu.get_declaration_interior(token_line)
        if declaration_interior is None:
            self.tokenizer.syntax_error("Couldn't find a valid unit declaration.")

        try:
            pu.check_declaration_validity(declaration_interior)
        except SyntaxError as e:
            self.tokenizer.syntax_error(str(e))

        unit_name = pu.find_name(declaration_interior)
        modifiers = pu.find_modifiers_decl(declaration_interior)
        nb_examples_asked = None
        if unit_type == pu.UnitType.intent:
            annotation_interior = pu.get_annotation_interior(token_line)
            if annotation_interior is not None and len(annotation_interior) > 0:
                nb_examples_asked = pu.find_nb_examples_asked(annotation_interior)

        self.create_unit(unit_type, unit_name, modifiers, nb_examples_asked)
        self._currently_parsed_declaration = (unit_type, unit_name, modifiers)

    def create_unit(self, unit_type, unit_name, modifiers,
                    nb_examples_asked=None):
        """
        Creates a unit of type `unit_type` with name `unit_name` and modifiers
        `modifiers` inside the AST.
        `modifiers` is a `UnitDeclarationModifiersRepr` and `nb_examples_asked`
        is a tuple (training, test).
        """
        # NOTE: this if-else statement is also done in the function it calls
        if unit_type == pu.UnitType.alias:
            new_unit = AliasDefinition(unit_name, modifiers)
            self.ast.stats.increment_aliases()
        elif unit_type == pu.UnitType.slot:
            new_unit = SlotDefinition(unit_name, modifiers)
            self.ast.stats.increment_slots()
        elif unit_type == pu.UnitType.intent:
            new_unit = IntentDefinition(unit_name, modifiers)
            self.ast.stats.increment_intents()

        if unit_type == pu.UnitType.intent and nb_examples_asked is not None:
            (train_nb, test_nb) = nb_examples_asked
            new_unit.set_nb_examples_asked(train_nb, test_nb)
        
        try:
            self.ast.add_unit(unit_type, unit_name, new_unit)
        except ValueError as e:  # NOTE: can be a new variation
            pass


    def _parse_rule(self, tokens):
        """
        Parses the list of string `tokens` that represents a rule in a
        template file and
        add the rule to the declaration currently being parsed.
        """
        if self._currently_parsed_declaration is None:
            self.tokenizer.syntax_error("Found a rule outside of "+
                                        "a unit declaration.")

        self._check_indentation(tokens[0])
        sub_rules = self.tokens_to_sub_rules(tokens[1:])

        unit_type = self._currently_parsed_declaration[0]
        name = self._currently_parsed_declaration[1]
        variation_name = self._currently_parsed_declaration[2].variation_name

        self.ast.add_rule_to_unit(unit_type, name, variation_name, sub_rules)

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

    def tokens_to_sub_rules(self, tokens):
        """Transforms a list of tokens into a list of sub-rules"""
        # Remove alternative slot rule if necessary
        alt_slot_value = None  # TODO DummySlotVal absolutely need to be managed differently
        if self._currently_parsed_declaration[0] == pu.UnitType.slot:
            answer = pu.find_alt_slot_and_index(tokens)
            if answer is not None:
                (end_index, alt_slot_value) = answer
                tokens = tokens[:end_index]

        sub_rules = []
        leading_space = False
        for sub_rule_tokens in pu.next_sub_rule_tokens(tokens):
            if len(sub_rule_tokens) == 1 and sub_rule_tokens[0] == ' ':
                leading_space = True
                continue

            sub_rule = self._make_sub_rule_from_tokens(sub_rule_tokens,
                                                       leading_space)
            if alt_slot_value is not None:
                if alt_slot_value != pu.ALT_SLOT_VALUE_FIRST_SYM:
                    sub_rules = [DummySlotValRuleContent(alt_slot_value, sub_rule)]
                else:
                    sub_rules = [DummySlotValRuleContent(sub_rule.name, sub_rule)]
                alt_slot_value = None
            sub_rules.append(sub_rule)

            leading_space = False
        return sub_rules

    def _make_sub_rule_from_tokens(self, sub_rule_tokens, leading_space):
        if pu.is_sub_rule_word(sub_rule_tokens):
            word_text = pu.remove_escapement(sub_rule_tokens[0])
            word = WordRuleContent(word_text, leading_space)
            return word
        if pu.is_sub_rule_word_group(sub_rule_tokens):
            group_interior_tokens = sub_rule_tokens[1:-1]
            self._check_sub_rule_validity(group_interior_tokens,
                                          pu.SubRuleType.word_group)
            words = pu.find_words(group_interior_tokens)
            words_str = pu.remove_escapement(''.join(words))
            modifiers = pu.find_modifiers_word_group(group_interior_tokens)
            word_group = \
                GroupWordRuleContent(words_str, leading_space,
                                     casegen=modifiers.casegen,
                                     randgen=modifiers.randgen_name,
                                     percentage_gen=modifiers.percentage_randgen)
            return word_group
        if pu.is_sub_rule_choice(sub_rule_tokens):
            choice_interior_tokens = sub_rule_tokens[1:-1]
            self._check_sub_rule_validity(choice_interior_tokens,
                                          pu.SubRuleType.choice)
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
                    if choice_sub_rule_tokens == [' ']:
                        current_leading_space = True
                        continue
                    choice_sub_rule = \
                        self._make_sub_rule_from_tokens(choice_sub_rule_tokens,
                                                        current_leading_space)
                    current_choice_sub_rules.append(choice_sub_rule)
                    current_leading_space = False
                choice.add_choice(current_choice_sub_rules)
            return choice

        if (   len(sub_rule_tokens) == 0
            or not pu.is_unit_type_sym(sub_rule_tokens[0])):
            # Not any type of sub-rule detected
            self.tokenizer.syntax_error("Invalid type of sub-rule.",
                                        word_to_find=sub_rule_tokens[0])

        interior_tokens = sub_rule_tokens[2:-1]
        name = pu.find_name(interior_tokens)
        if pu.is_sub_rule_alias_ref(sub_rule_tokens):
            self._check_sub_rule_validity(interior_tokens,
                                          pu.SubRuleType.alias)
            modifiers = pu.find_modifiers_reference(interior_tokens)
            alias = AliasRuleContent(name, leading_space,
                                     modifiers.variation_name,
                                     modifiers.argument_value,
                                     modifiers.casegen,
                                     modifiers.randgen_name,
                                     modifiers.percentage_randgen, self)
            return alias
        if pu.is_sub_rule_slot_ref(sub_rule_tokens):
            self._check_sub_rule_validity(interior_tokens,
                                          pu.SubRuleType.slot)
            modifiers = pu.find_modifiers_reference(interior_tokens)
            slot = SlotRuleContent(name, leading_space,
                                   modifiers.variation_name,
                                   modifiers.argument_value,
                                   modifiers.casegen,
                                   modifiers.randgen_name,
                                   modifiers.percentage_randgen, self)
            return slot
        if pu.is_sub_rule_intent_ref(sub_rule_tokens):
            self._check_sub_rule_validity(interior_tokens,
                                          pu.SubRuleType.intent)
            modifiers = pu.find_modifiers_reference(interior_tokens)
            intent = IntentRuleContent(name, leading_space,
                                       modifiers.variation_name,
                                       modifiers.argument_value,
                                       modifiers.casegen,
                                       modifiers.randgen_name,
                                       modifiers.percentage_randgen, self)
            return intent

    def _check_sub_rule_validity(self, interior_tokens, sub_rule_type):
        """
        Checks that the sub-rule represented by `interior_tokens` is
        syntactically valid.
        """
        try:
            if sub_rule_type == pu.SubRuleType.word_group:
                pu.check_word_group_validity(interior_tokens)
            elif sub_rule_type == pu.SubRuleType.choice:
                pu.check_choice_validity(interior_tokens)
            elif sub_rule_type in (pu.SubRuleType.alias,
                                   pu.SubRuleType.slot,
                                   pu.SubRuleType.intent):
                pu.check_reference_validity(interior_tokens)
        except SyntaxError as e:
            self.tokenizer.syntax_error(str(e))


