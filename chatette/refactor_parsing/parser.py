"""
Module `chatette.refactor_parsing.parser`
Contains the definition of the parser
that is in charge of parsing the different template files
and to produce an Abstract Syntax Tree that represents the information from 
those files.
"""

from six import string_types

from chatette.refactor_parsing.input_file_manager import InputFileManager
from chatette.refactor_parsing.lexer import Lexer


class Parser(object):
    def __init__(self, master_filename):
        if not isinstance(master_filename, string_types):
            raise ValueError(
                "Since v1.4.0, the parser takes as an argument " + \
                "the path of the master file directly, rather " + \
                "than the file itself as before.")
        self.input_file_manager = InputFileManager.get_or_create(master_filename)
        self.lexer = Lexer()
    

    def parse(self):
        """
        Parses the template file(s) and translates them into an AST.
        """
        while True:
            line = self.input_file_manager.next_line()
            if line is None:
                break
            print("LINE:", str(line))
            lexed_line = self.lexer.lex(line)
            print(lexed_line)
