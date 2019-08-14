# coding: utf-8
"""
Module `chatette.refactor_parsing.parser`
Contains the definition of the parser
that is in charge of parsing the different template files
and to produce an Abstract Syntax Tree that represents the information from 
those files.
"""

from __future__ import print_function
from six import string_types

from chatette.utils import print_DBG, print_warn, UnitType
from chatette.refactor_parsing import utils

from chatette.refactor_parsing.input_file_manager import InputFileManager
from chatette.refactor_parsing.lexing.lexer import Lexer
from chatette.refactor_parsing.lexing import TerminalType
from chatette.refactor_units.ast import AST

from chatette.modifiers.representation import ModifiersRepresentation
from chatette.refactor_units.definitions.alias import AliasDefinition
from chatette.refactor_units.definitions.slot import SlotDefinition
from chatette.refactor_units.definitions.intent import IntentDefinition
from chatette.refactor_units.word import Word
from chatette.refactor_units.choice import Choice
from chatette.refactor_units.unit_reference import UnitReference
from chatette.refactor_units.rule import Rule

from chatette.refactor_parsing import ChoiceBuilder, UnitRefBuilder


class Parser(object):
    def __init__(self, master_file_path):
        if not isinstance(master_file_path, string_types):
            raise ValueError(
                "Since v1.4.0, the parser takes as an argument " + \
                "the path of the master file directly, rather " + \
                "than the file itself as before.")
        self._master_filepath = master_file_path

        self.input_file_manager = \
            InputFileManager.get_or_create(master_file_path)
        self.lexer = Lexer()
        self.ast = AST.get_or_create()

        self._declaration_line_allowed = True
        self._last_indentation = None
        self._current_unit_declaration = None
    

    def parse(self):
        """
        Parses the template file(s) and translates them into an AST.
        """
        print_DBG(
            "Parsing master file: " + \
            self.input_file_manager.get_current_file_name()
        )

        while True:
            line = self.input_file_manager.read_line()
            if line is None:  # End of file
                break
            print("\nLINE: '" + str(line) + "'")
            lexical_tokens = self.lexer.lex(line)
            print("TOKENS:", lexical_tokens)
            lexical_tokens = utils.remove_comment_tokens(lexical_tokens)

            if len(lexical_tokens) == 0:
                continue

            if lexical_tokens[0].type == TerminalType.file_inclusion_marker:
                self._parse_file_inclusion(lexical_tokens)
                self._declaration_line_allowed = True
                self._last_indentation = None
            elif lexical_tokens[0].type == TerminalType.indentation:
                self._parse_rule_line(lexical_tokens)
                self._declaration_line_allowed = True
                self._last_indentation = lexical_tokens[0].text
            elif (
                lexical_tokens[0].type in \
                (TerminalType.alias_decl_start,
                 TerminalType.slot_decl_start,
                 TerminalType.intent_decl_start)
            ):
                self._parse_unit_declaration(lexical_tokens)
                self._declaration_line_allowed = False
                self._last_indentation = None
            else:
                self.input_file_manager.syntax_error(
                    "Couldn't parse this line: a line can be either " + \
                    "an empty line, a comment line, a file inclusion line, " + \
                    "a unit declaration or a rule."
                )
            print("AST")
            self.ast.print_DBG()

    def _parse_file_inclusion(self, lexical_tokens):
        """
        Opens the file that is included by the tokenized line `lexical_tokens`.
        @pre: `lexical_tokens` contain a tokenized file inclusion line.
        """
        try:
            self.input_file_manager.open_file(lexical_tokens[1].text)
            print(
                "Parsing file: " + \
                self.input_file_manager.get_current_file_name()
            )
        except IOError as e:
            print_warn(
                "There was an error while opening file '" + \
                lexical_tokens[1].text + "': " + str(e) + \
                "\nContinuing the parsing of '" + \
                self.input_file_manager.get_current_file_name() + "'."
            )
        except ValueError as e:
            print_warn(
                str(e) + "\nContinuing the parsing of '" + \
                self.input_file_manager.get_current_file_name() + "'."
            )

    def _parse_unit_declaration(self, lexical_tokens):
        """
        Handles the tokens `lexical tokens` that contain a unit declaration.
        """
        # TODO this code doesn't seem very clean (should refactor)
        if not self._declaration_line_allowed:
            self.input_file_manager.syntax_error(
                "Didn't expect a unit declaration to start here."
            )

        i = 0

        unit_decl_class = None
        identifier = None
        modifiers = ModifiersRepresentation()

        if lexical_tokens[i].type == TerminalType.alias_decl_start:
            unit_decl_class = AliasDefinition
            add_unit_def_function = self.ast.add_alias
        elif lexical_tokens[i].type == TerminalType.slot_decl_start:
            unit_decl_class = SlotDefinition
            add_unit_def_function = self.ast.add_slot
        elif lexical_tokens[i].type == TerminalType.intent_decl_start:
            unit_decl_class = IntentDefinition
            add_unit_def_function = self.ast.add_intent
        else:  # Should never happen
            raise ValueError(
                "Tried to parse a line as if it was a unit declaration " + \
                "while it wasn't."
            )
        
        i += 1
        if lexical_tokens[i].type == TerminalType.casegen_marker:
            modifiers.casegen = True
            i += 1
        
        if lexical_tokens[i].type == TerminalType.unit_identifier:
            identifier = lexical_tokens[i].text
            i += 1
        else:  # Should never happen
            self.input_file_manager.syntax_error(
                "The unit declared here doesn't seem to have an identifier. " + \
                "All units must have an identifier."
            )
        
        expecting_variation_name = False
        expecting_randgen_name = False
        expecting_percent = False
        expecting_arg_name = False
        for token in lexical_tokens[i:]:
            if expecting_variation_name:
                if token.type == TerminalType.variation_name:
                    modifiers.variation = token.text
                else:  # Should never happen
                    self.input_file_manager.syntax_error(
                        "Couldn't extract the name of the variation."
                    )
                expecting_variation_name = False
            elif expecting_randgen_name:
                if token.type == TerminalType.randgen_name:
                    modifiers.randgen_name = token.text
                expecting_randgen_name = False
            elif expecting_percent:
                if token.type == TerminalType.percentgen:
                    try:
                        modifiers.randgen_percent = float(token.text)
                    except ValueError as e:  # Should never happen
                        self.input_file_manager.syntax_error(
                            "Couldn't understand the percentage for " + \
                            "the random generation modifier: " + str(e)
                        )
                else:  # Should never happen
                    self.input_file_manager.syntax_error(
                        "Couldn't extract the percentage for " + \
                        "the random generation modifier."
                    )
                expecting_percent = False
            elif expecting_arg_name:
                if token.type == TerminalType.arg_name:
                    modifiers.argument_name = token.text
                else:  # Should never happen
                    self.input_file_manager.syntax_error(
                        "Couldn't extract the name of " + \
                        "the argument modifier."
                    )
                expecting_arg_name = False
            elif token.type == TerminalType.variation_marker:
                expecting_variation_name = True
            elif token.type == TerminalType.randgen_marker:
                modifiers.randgen = True
                expecting_randgen_name = True
            elif token.type == TerminalType.percentgen_marker:
                expecting_percent = True
            elif token.type == TerminalType.arg_marker:
                expecting_arg_name = True
            elif (
                token.type in \
                (TerminalType.alias_decl_end,
                 TerminalType.slot_decl_end,
                 TerminalType.intent_decl_end)
            ):
                break
            else:  # Should never happen
                self.input_file_manager.syntax_error(
                    "Invalid token type (" + str(token.type) + ") for '" + \
                    token.text + "'."
                )

        annotation_tokens = utils.extract_annotation_tokens(lexical_tokens)
        annotation = None
        if annotation_tokens is not None and unit_decl_class != IntentDefinition:
            if unit_decl_class == AliasDefinition:
                unit_type = "alias"
            else:
                unit_type = "slot"
            print_warn(
                "Found an annotation when parsing " + unit_type + " '" + \
                identifier + "'\n" + \
                "Annotations are currently only supported for intent " + \
                "definitions. Any other annotation is ignored."
            )
        elif annotation_tokens is not None:
            annotation = self._annotation_tokens_to_dict(annotation_tokens)
        
        unit = unit_decl_class(identifier)
        if annotation is not None:  # parsing intent
            (nb_training_ex, nb_testing_ex) = \
                self._parse_intent_annotation(annotation)
            unit.set_nb_examples_asked(nb_training_ex, nb_testing_ex)
        
        add_unit_def_function(unit)
        self._current_unit_declaration = unit

    def _parse_intent_annotation(self, annotation):
        """
        Given a dict representing the annotation corresponding to an intent
        declaration, returns the number of examples asked in the training
        and testing sets (as a 2-tuple).
        Returns `None` instead of a number if a number was not provided.
        @raises - `SyntaxError` if the number of examples provided are
                  actually not integral numbers.
                - `SyntaxError` if the annotation contains the same information
                  at least twice.
        Prints a warning if the annotation contains unrecognized keys.
        """
        nb_training_ex = None
        nb_testing_ex = None
        for key in annotation:
            if key is None or key.lower() in ("training", "train"):
                if nb_training_ex is not None:
                    self.input_file_manager.syntax_error(
                        "Detected a number of examples for training set " + \
                        "several times."
                    )
                nb_training_ex = \
                    self._str_to_int(
                        annotation[key],
                        "Couldn't parse the annotation of the intent."
                    )
            elif key.lower() in ("testing", "test"):
                if nb_testing_ex is not None:
                    self.input_file_manager.syntax_error(
                        "Detected a number of examples for testing set " + \
                        "several times."
                    )
                nb_testing_ex = \
                    self._str_to_int(
                        annotation[key],
                        "Couldn't parse the annotation of the intent."
                    )
            else:
                print_warn("Unsupported key in the annotation: '" + key + "'.")
        return (nb_training_ex, nb_testing_ex)
    def _annotation_tokens_to_dict(self, tokens):
        """
        Transforms the tokens `tokens` that contain an annotation into a dictionary
        that contains the same information.
        @pre: `tokens` really contains an annotation (starting at the beginning of
            the list).
        @raises: - `ValueError` if the precondition is not met.
                - `SyntaxError` if the annotation contains the same key twice.
        """
        if len(tokens) == 0 or tokens[0].type != TerminalType.annotation_start:
            raise ValueError(
                "Tried to parse tokens as if they were an annotation while " + \
                "they weren't"
            )

        result = dict()
        current_key = None
        for token in tokens:
            if token.type == TerminalType.annotation_end:
                break
            elif token.type == TerminalType.key:
                current_key = token.text
            elif token.type == TerminalType.value:
                if current_key in result:
                    self.input_file_manager.syntax_error(
                        "Annotation contained the key '" + current_key + \
                        "' twice."
                    )
                result[current_key] = token.text

        return result
    def _str_to_int(self, text, err_msg):
        """
        Transforms the str `text` into an int.
        @raises: `SyntaxError` with the message `err_msg` and a small message
                 explaining `text` is not a valid int
                 if the cast couldn't be performed.
        """
        try:
            return int(text)
        except ValueError:
            self.input_file_manager.syntax_error(
                err_msg + " '" + text + "' is not a valid integral number."
            )

    def _parse_rule_line(self, lexical_tokens):
        """
        Handles a line that is a rule within a unit definition.
        Adds the rule to the currently parsed unit.
        """
        if (
            self._last_indentation is not None
            and lexical_tokens[0].text != self._last_indentation
        ):
            self.input_file_manager.syntax_error("Inconsistent indentation.")
        
        rule = self._parse_rule(lexical_tokens[1:])
        self._current_unit_declaration.add_rule(rule)

    def _parse_rule(self, tokens):
        """
        Handles the tokens `tokens` that contain a rule (inside a unit
        definition).
        Returns the rule (`Rule`) that `tokens` represent.
        """
        rule_contents = []
        current_repr = None
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.type == TerminalType.whitespace:
                # TODO put it in modifiers
                if current_repr is not None:
                    rule_contents.append(current_repr.create_concrete())
                    current_repr = None
            # Units and rule contents
            elif token.type == TerminalType.word:
                rule_contents.append(Word(token.text))
            elif (
                token.type in \
                (TerminalType.alias_ref_start,
                    TerminalType.slot_ref_start,
                    TerminalType.intent_ref_end)
            ):
                if current_repr is not None:
                    rule_contents.append(current_repr.create_concrete())
                current_repr = UnitRefBuilder()
                if token.type == TerminalType.alias_ref_start:
                    current_repr.type = UnitType.alias
                elif token.type == TerminalType.slot_ref_start:
                    current_repr.type = UnitType.slot
                elif token.type == TerminalType.intent_ref_start:
                    current_repr.type = UnitType.intent
            elif (
                token.type in \
                (TerminalType.alias_ref_end,
                 TerminalType.slot_ref_end,
                 TerminalType.intent_ref_end)
            ):
                rule_contents.append(current_repr.create_concrete())
                current_repr = None
            elif token.type == TerminalType.unit_identifier:
                current_repr.identifier = token.text
            elif token.type == TerminalType.choice_start:
                if current_repr is not None:
                    rule_contents.append(current_repr.create_concrete())
                current_repr = ChoiceBuilder()
                end_choice_index = utils.find_matching_choice_end(tokens, i)
                if end_choice_index is not None:
                    internal_rules = \
                        self._parse_choice(tokens[i:end_choice_index + 1])
                    current_repr.rules = internal_rules
                    i = end_choice_index
                else:
                    self.input_file_manager.syntax_error(
                        "Inconsistent choice starts and endings."
                    )
            elif token.type == TerminalType.choice_end:
                rule_contents.append(current_repr.create_concrete())
            # Modifiers
            elif token.type == TerminalType.casegen_marker:
                current_repr.casegen = True
            elif token.type == TerminalType.randgen_marker:
                current_repr.randgen = True
            elif token.type == TerminalType.randgen_name:
                current_repr.randgen_name = token.text
            elif token.type == TerminalType.variation_marker:
                pass
            elif token.type == TerminalType.variation_name:
                current_repr.variation = token.text
            elif token.type == TerminalType.arg_marker:
                pass
            elif token.type == TerminalType.arg_value:
                current_repr.arg_value = token.text
            i += 1
        if current_repr is not None:
            rule_contents.append(current_repr.create_concrete())

        return Rule(self._current_unit_declaration.full_name, rule_contents)

    def _parse_choice(self, tokens):
        tokens = tokens[1:-1]
        rules = []

        current_rule_start_index = 0
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.type == TerminalType.choice_sep:
                rules.append(
                    self._parse_rule(tokens[current_rule_start_index:i])
                )
                current_rule_start_index = i+1
            if token.type == TerminalType.choice_start:
                end_choice_index = utils.find_matching_choice_end(tokens, i)
                if end_choice_index is None:
                    self.input_file_manager.syntax_error(
                        "Inconsistent choice starts and endings."
                    )
                i = end_choice_index
            i += 1

        if i > 0 and tokens[i-1].type == TerminalType.percentgen:
            i -= 1
        if i > 0 and tokens[i-1].type == TerminalType.percentgen_marker:
            i -= 1
        if i > 0 and tokens[i-1].type == TerminalType.randgen_name:
            i -= 1
        if i > 0 and tokens[i-1].type == TerminalType.randgen_marker:
            i -= 1
        rules.append(
            self._parse_rule(tokens[current_rule_start_index:i])
        )

        return rules
