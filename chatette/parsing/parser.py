# coding: utf-8
"""
Module `chatette.parsing.parser`
Contains the definition of the parser
that is in charge of parsing the different template files
and to produce an Abstract Syntax Tree that represents the information from 
those files.
"""

from __future__ import print_function
from six import string_types

from chatette.utils import print_DBG, print_warn, UnitType, cast_to_unicode
from chatette.parsing import utils
from chatette.parsing.lexing import \
    remove_comment_tokens, find_matching_choice_end, \
    find_index_last_choice_content
from chatette.statistics import Stats

from chatette.parsing.input_file_manager import \
    InputFileManager, FileAlreadyOpened
from chatette.parsing.lexing.lexer import Lexer
from chatette.parsing.lexing import TerminalType
from chatette.units.ast import AST

from chatette.units.modifiable.definitions.alias import AliasDefinition
from chatette.units.modifiable.definitions.slot import SlotDefinition
from chatette.units.modifiable.definitions.intent import IntentDefinition
from chatette.units.word import Word
from chatette.units.rule import Rule

from chatette.parsing import \
    ChoiceBuilder, UnitRefBuilder, \
    AliasDefBuilder, SlotDefBuilder, IntentDefBuilder


class Parser(object):
    def __init__(self, master_file_path=None):
        if (
            master_file_path is not None
            and not isinstance(master_file_path, string_types)
        ):
            raise ValueError(
                "Since v1.4.0, the parser takes as an argument " + \
                "the path of the master file directly, rather " + \
                "than the file itself as before.")
        self._master_filepath = master_file_path

        self.input_file_manager = \
            InputFileManager.get_or_create()
        self.lexer = Lexer()
        self.ast = AST.get_or_create()

        self._declaration_line_allowed = True
        self._last_indentation = None

        self._current_unit_declaration = None
        self._current_variation_name = None
    

    def open_new_file(self, filepath):
        """Opens the new (master) file, making the parser ready to parse it."""
        try:
            self.input_file_manager.open_file(filepath)
        except IOError as e:
            raise IOError(
                "There was an error while opening file '" + \
                str(cast_to_unicode(filepath)) + "': " + str(e) + "."
            )
        except FileAlreadyOpened as e:
            err_msg = str(e)
            current_file_name = self.input_file_manager.get_current_file_name()
            if current_file_name is not None:
                err_msg += \
                    "\nContinuing the parsing of '" + str(current_file_name) + \
                    "'."
            print_warn(err_msg)
    

    def parse_file(self, file_path):
        """
        Parses the template file(s) at `file_path`
        and translates them into an AST.
        """
        self.open_new_file(file_path)
        print_DBG(
            "Parsing file: " + \
            self.input_file_manager.get_current_file_name()
        )

        while True:
            line = self.input_file_manager.read_line()
            if line is None:  # End of file
                break
            currently_parsing_slot = (
                self._current_unit_declaration is not None
                and self._current_unit_declaration.unit_type == UnitType.slot
            )
            lexical_tokens = self.lexer.lex(line, currently_parsing_slot)
            lexical_tokens = remove_comment_tokens(lexical_tokens)

            if len(lexical_tokens) == 0:
                continue

            if lexical_tokens[0].type == TerminalType.file_inclusion_marker:
                self._parse_file_inclusion(lexical_tokens)
                self._declaration_line_allowed = True
                self._last_indentation = None
                self._current_unit_declaration = None
                self._current_variation_name = None
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
                self._parse_unit_declaration_line(lexical_tokens)
                self._declaration_line_allowed = False
                self._last_indentation = None
            else:
                self.input_file_manager.syntax_error(
                    "Couldn't parse this line: a line can be either " + \
                    "an empty line, a comment line, a file inclusion line, " + \
                    "a unit declaration or a rule."
                )


    def _parse_file_inclusion(self, lexical_tokens):
        """
        Opens the file that is included by the tokenized line `lexical_tokens`.
        @pre: `lexical_tokens` contain a tokenized file inclusion line.
        """
        self.open_new_file(lexical_tokens[1].text)
        print_DBG(
            "Parsing file: " + \
            self.input_file_manager.get_current_file_name()
        )


    def _parse_unit_declaration_line(self, line_tokens):
        """
        Parses the tokens `line_tokens` that correspond to a whole line
        where a unit is declared.
        Adds the definition to the AST.
        """
        if not self._declaration_line_allowed:
            self.input_file_manager.syntax_error(
                "Didn't expect a unit declaration to start here."
            )

        (unit, variation) = self._parse_unit_declaration(line_tokens)

        try:
            self.ast.add_unit(unit)
        except ValueError as e:
            if variation is None:
                self.input_file_manager.syntax_error(str(e))
            elif variation in self.ast[unit.unit_type][unit.identifier]:
                self.input_file_manager.syntax_error(
                    "Variation '" + str(variation) + "' was already " + \
                    "declared for " + unit.full_name + "."
                )
            else:  # new variation was declared
                pass
        self._current_variation_name = variation
        self._current_unit_declaration = unit

    def _parse_unit_declaration(self, lexical_tokens):
        """
        Parses the tokens `lexical_tokens` that contain a unit declaration.
        Returns the corresponding concrete unit.
        """
        if lexical_tokens[0].type == TerminalType.alias_decl_start:
            builder = AliasDefBuilder()
        elif lexical_tokens[0].type == TerminalType.slot_decl_start:
            builder = SlotDefBuilder()
        elif lexical_tokens[0].type == TerminalType.intent_decl_start:
            builder = IntentDefBuilder()
        else:  # Should never happen
            raise ValueError(
                "Tried to parse a line as if it was a unit declaration " + \
                "while it wasn't."
            )
        
        i = 1
        while i < len(lexical_tokens):
            token = lexical_tokens[i]
            if token.type == TerminalType.unit_identifier:
                builder.identifier = token.text
            elif token.type == TerminalType.casegen_marker:
                builder.casegen = True
            elif token.type == TerminalType.randgen_marker:
                builder.randgen = True
            elif token.type == TerminalType.randgen_name:
                builder.randgen_name = token.text
            elif token.type == TerminalType.variation_marker:
                pass
            elif token.type == TerminalType.variation_name:
                builder.variation = token.text
            elif token.type == TerminalType.arg_marker:
                pass
            elif token.type == TerminalType.arg_name:
                builder.arg_name = token.text
            elif (
                token.type in \
                (TerminalType.alias_decl_end,
                 TerminalType.slot_decl_end,
                 TerminalType.intent_decl_end)
            ):
                i += 1
                break
            else:
                raise ValueError(  # Should never happen
                    "Detected invalid token type in unit definition: " + \
                    token.type.name
                )
            i += 1


        if (
            i < len(lexical_tokens)
            and lexical_tokens[i].type == TerminalType.annotation_start
        ):
            if not isinstance(builder, IntentDefBuilder):
                if isinstance(builder, AliasDefBuilder):
                    unit_type = "alias"
                else:
                    unit_type = "slot"
                print_warn(
                    "Found an annotation when parsing " + unit_type + " '" + \
                    identifier + "'\n" + \
                    "Annotations are currently only supported for intent " + \
                    "definitions. Any other annotation is ignored."
                )
            else:
                annotation_tokens = lexical_tokens[i:]
                annotation = self._annotation_tokens_to_dict(annotation_tokens)
                (nb_training_ex, nb_testing_ex) = \
                    self._parse_intent_annotation(annotation)
                builder.nb_training_ex = nb_training_ex
                builder.nb_testing_ex = nb_testing_ex
        
        return (builder.create_concrete(), builder.variation)

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
        if self._current_unit_declaration is None:
            self.input_file_manager.syntax_error(
                "Detected a rule outside a unit declaration."
            )
        
        rule = self._parse_rule(lexical_tokens[1:])
        self._current_unit_declaration.add_rule(
            rule, self._current_variation_name
        )

        Stats.get_or_create().new_rule_parsed()

    def _parse_rule(self, tokens):
        """
        Handles the tokens `tokens` that contain a rule (inside a unit
        definition).
        Returns the rule (`Rule`) that `tokens` represent.
        """
        # TODO replace this with a (stateful) iterator to make it more readable
        rule_contents = []
        current_builder = None
        leading_space = False
        slot_value = None
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.type == TerminalType.whitespace:
                leading_space = True
                if current_builder is not None:
                    rule_contents.append(current_builder.create_concrete())
                    current_builder = None
            # Units and rule contents
            elif token.type == TerminalType.word:
                rule_contents.append(Word(token.text, leading_space))
                leading_space = False
            elif (
                token.type in \
                (TerminalType.alias_ref_start,
                    TerminalType.slot_ref_start,
                    TerminalType.intent_ref_end)
            ):
                if current_builder is not None:
                    rule_contents.append(current_builder.create_concrete())
                current_builder = UnitRefBuilder()
                current_builder.leading_space = leading_space
                if token.type == TerminalType.alias_ref_start:
                    current_builder.type = UnitType.alias
                elif token.type == TerminalType.slot_ref_start:
                    current_builder.type = UnitType.slot
                elif token.type == TerminalType.intent_ref_start:
                    current_builder.type = UnitType.intent
            elif (
                token.type in \
                (TerminalType.alias_ref_end,
                 TerminalType.slot_ref_end,
                 TerminalType.intent_ref_end)
            ):
                rule_contents.append(current_builder.create_concrete())
                current_builder = None
                leading_space = False
            elif token.type == TerminalType.unit_identifier:
                current_builder.identifier = token.text
            elif token.type == TerminalType.choice_start:
                if current_builder is not None:
                    rule_contents.append(current_builder.create_concrete())
                current_builder = ChoiceBuilder()
                current_builder.leading_space = leading_space
                last_internal_choice_token = \
                    find_index_last_choice_content(tokens, i)
                if last_internal_choice_token is not None:
                    i += 1
                    if tokens[i].type == TerminalType.casegen_marker:
                        current_builder.casegen = True
                        i += 1
                    internal_rules = \
                        self._parse_choice(
                            tokens[i:last_internal_choice_token + 1]
                        )
                    current_builder.rules = internal_rules
                    i = last_internal_choice_token
                else:
                    self.input_file_manager.syntax_error(
                        "Inconsistent choice start and ending."
                    )
            elif token.type == TerminalType.choice_end:
                rule_contents.append(current_builder.create_concrete())
                current_builder = None
                leading_space = False
            # Modifiers
            elif token.type == TerminalType.casegen_marker:
                current_builder.casegen = True
            elif token.type == TerminalType.randgen_marker:
                current_builder.randgen = True
            elif token.type == TerminalType.opposite_randgen_marker:
                current_builder.randgen_opposite = True
            elif token.type == TerminalType.randgen_name:
                current_builder.randgen_name = token.text
            elif token.type == TerminalType.percentgen_marker:
                pass
            elif token.type == TerminalType.percentgen:
                current_builder.randgen_percent = \
                    self._str_to_int(
                        token.text,
                        "Couldn't parse the percentage " + \
                        "for the random generation modifier."
                    )
            elif token.type == TerminalType.variation_marker:
                pass
            elif token.type == TerminalType.variation_name:
                current_builder.variation = token.text
            elif token.type == TerminalType.arg_marker:
                pass
            elif token.type == TerminalType.arg_value:
                current_builder.arg_value = token.text
            elif token.type == TerminalType.slot_val_marker:
                pass
            elif token.type == TerminalType.slot_val:
                slot_value = token.text
            else:
                raise ValueError(  # Should never happen
                    "Detected invalid token type in rule: " + \
                    token.type.name + " for text '" + token.text + "'."
                )
            i += 1
        if current_builder is not None:
            rule_contents.append(current_builder.create_concrete())

        if self._current_unit_declaration is not None:
            return Rule(
                self._current_unit_declaration.full_name,
                rule_contents, slot_value
            )
        # NOTE can only come from an interactive command (the 'rule' command)
        return Rule(None, rule_contents, slot_value)

    def _parse_choice(self, tokens):
        rules = []

        current_rule_start_index = 0
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.type == TerminalType.choice_sep:
                rules.append(
                    self._parse_rule(tokens[current_rule_start_index:i])
                )
                current_rule_start_index = i + 1
            if token.type == TerminalType.choice_start:
                end_choice_index = find_matching_choice_end(tokens, i)
                if end_choice_index is None:
                    self.input_file_manager.syntax_error(
                        "Inconsistent choice starts and endings."
                    )
                i = end_choice_index
            i += 1

        rules.append(
            self._parse_rule(tokens[current_rule_start_index:i])
        )

        return rules
