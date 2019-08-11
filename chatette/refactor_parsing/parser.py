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
from chatette.refactor_parsing.utils import remove_comment_tokens

from chatette.refactor_parsing.input_file_manager import InputFileManager
from chatette.refactor_parsing.lexing.lexer import Lexer
from chatette.refactor_parsing.lexing import TerminalType


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
        self._declaration_line_allowed = False
    def _parse_rule(self, lexical_tokens):
        """
        Handles the tokens `lexical tokens` that contain a rule (inside a unit
        definition).
        """
        print("Rule")
        self._declaration_line_allowed = True
