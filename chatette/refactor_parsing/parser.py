# -*- coding: utf-8 -*-
"""
Module `chatette.refactor_parsing.parser`
Contains the definition of the parser
that is in charge of parsing the different template files
and to produce an Abstract Syntax Tree that represents the information from 
those files.
"""

from __future__ import print_function
from six import string_types

from chatette.refactor_parsing.input_file_manager import InputFileManager
from chatette.refactor_parsing.lexing.lexer import Lexer


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
    

    def parse(self):
        """
        Parses the template file(s) and translates them into an AST.
        """
        while True:
            line = self.input_file_manager.read_line()
            if line is None:
                break
            print("\nLINE:", str(line))
            lexed_line = self.lexer.lex(line)
            print("TOKENS:", lexed_line)
