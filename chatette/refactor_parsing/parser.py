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

from chatette.utils import print_DBG, print_warn
from chatette.refactor_parsing.utils import \
    remove_comment_tokens, extract_annotation_tokens

from chatette.refactor_parsing.input_file_manager import InputFileManager
from chatette.refactor_parsing.lexing.lexer import Lexer
from chatette.refactor_parsing.lexing import TerminalType

from chatette.refactor_units.definitions.alias import AliasDefinition
from chatette.refactor_units.definitions.slot import SlotDefinition
from chatette.refactor_units.definitions.intent import IntentDefinition
from chatette.modifiers.representation import ModifiersRepresentation


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

        self._declaration_line_allowed = True
    

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
            lexical_tokens = remove_comment_tokens(lexical_tokens)

            if len(lexical_tokens) == 0:
                continue

            if lexical_tokens[0].type == TerminalType.file_inclusion_marker:
                self._parse_file_inclusion(lexical_tokens)
            elif lexical_tokens[0].type == TerminalType.indentation:
                self._parse_rule(lexical_tokens)
            elif (
                lexical_tokens[0].type in \
                (TerminalType.alias_decl_start,
                 TerminalType.slot_decl_start,
                 TerminalType.intent_decl_start)
            ):
                self._parse_unit_declaration(lexical_tokens)
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
        print("Unit declaration")
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
        elif lexical_tokens[i].type == TerminalType.slot_decl_start:
            unit_decl_class = SlotDefinition
        elif lexical_tokens[i].type == TerminalType.intent_decl_start:
            unit_decl_class = IntentDefinition
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

        
        annotation_tokens = extract_annotation_tokens(lexical_tokens)
        if annotation_tokens is not None:
            annotation = annotation_tokens_to_dict(annotation_tokens)
        else:
            annotation = None
        
        
        self._declaration_line_allowed = False

    def _parse_rule(self, lexical_tokens):
        """
        Handles the tokens `lexical tokens` that contain a rule (inside a unit
        definition).
        """
        print("Rule")
        self._declaration_line_allowed = True


def annotation_tokens_to_dict(tokens):
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
                raise SyntaxError(
                    "Annotation contained the key '" + current_key + "' twice."
                )
            result[current_key] = token.text

    return result
