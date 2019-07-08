"""
Module `chatette.refactor_parsing`
Contains the lexer used by the parser and the definition of the tokens it uses.
"""

from enum import Enum

import chatette.parsing.parser_utils as pu
from chatette.parsing.line_count_file_wrapper impoprt LineCountFileWrapper

# Supported tokens
class TerminalTypes(enum):
    """Enum of terminals types that will be used by the lexer."""
    # File inclusion
    file_include_sym = 0
    file_path = 1
    # Unit declarations
    intent_decl_start = 2
    intent_decl_end = 3
    slot_decl_start = 4
    slot_decl_end = 5
    alias_decl_start = 6
    alias_decl_end = 7
    # Annotations
    annotation_start = 24
    annotation_end = 25
    annotation_sep = 28
    key = 26
    value = 27
    key_value_connector = 32
    encloser = 33  # either " or '
    # Rule contents
    word = 8
    choice_start = 9
    choice_end = 10
    choice_sep = 11
    # Modifiers
    arg_decl_sym = 12
    arg_val_sym = 13
    arg_decl = 14
    arg_decl_sep = 29
    arg_name = 15
    arg_val = 16
    arg_connector = 34
    casegen = 17
    variation_sym = 18
    variation_name = 19
    randgen_sym = 20
    randgen_name = 21
    percentgen_sym = 22
    percentgen = 23
    # Spaces
    indentation = 30
    whitespace = 31
    comment = 35


class Lexer(object):
    """
    This class is intended to manage the opening and reading of the template
    files and to transform the read stream of characters into
    a stream of tokens and additional information (terminal type).
    """
    def __init__(self):
        self._current_file = None
        self._opened_files = []

        self._last_read_line = None  # str
    
    def open_file(self, filepath):
        opened_filepaths = [f.name for f in self._opened_files]
        if filepath in opened_filepaths:
            raise ValueError(
                "Tried to read file '" + filepath + "' several times."
            )
        self._current_file = LineCountFileWrapper(filepath)
        self._opened_files.append(filepath)
    
    def close_files(self):
        for f in self._opened_files:
            if not f.closed:
                f.close()
        if not self._current_file is not None and not self._current_file.closed:
            self._current_file.close()
    def _close_current_file(self):
        """
        Closes current file and
        sets current file to the file previously being read (if any).
        """
        if self._current_file is not None:
            self._current_file.close()
        if len(self._opened_files) > 0:
            self._current_file = self._opened_files.pop()
        else:
            self._current_file = None
    

    def get_current_file_information(self):
        return (self._current_file.name, self._current_file.line_nb)
    def get_current_filename(self):
        return self._current_file.name
    

    def syntax_error(self, message, line=None, line_index=0, word_to_find=None):
        """Closes all files and raises a `SyntaxError`."""
        if lin is None:
            line = self._last_read_line
        if word_to_find is not None and line is not None:
            line_index = line.find(word_to_find)
        
        self.close_files()
        raise SyntaxError(
            message,
            (self._current_file.name, self._current_file.line_nb,
             line_index, line)
        )


    def _read_line(self)
        """
        Reads a line of `self._current_file` and
        returns it the trailing new line (`\n`).
        If the file was entirely read, closes it and
        continues to read the file that was previously being read (if any).
        Returns `None` if there is no file left to read.
        """
        line = self._current_file.readline()
        while line == '':  # EOF
            self._close_current_file()
            if self._current_file is None:  # No more files to read
                return None
            line = self._current_file.readline()
        line = line.rstrip()
        self._last_read_line = line
        return line
    
    def next_tokenized_line(self):
        """
        Yields the next relevant line of the current file as a list of dict
        containing tokens and token types
        (`{"token-type": TerminalType, "token": str}`).
        An irrelevant line is an empty or comment line.
        """
        while True:
            line_str = pu.strip_comments(self._read_line())
            if line_str is None:
                break
            if line_str == "":
                continue
            yield self._tokenize(line_str)

    def _tokenize(self, text):
        """
        Returns a tokenized version of the string `text`,
        i.e. a list of dict containing tokens and token types
        (`{"token-type": TerminalType, "token": str}`).
        """
        tokens = []
    
    
