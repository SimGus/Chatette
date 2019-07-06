"""
Module `chatette.refactor_parsing`
Contains the lexer used by the parser and the definition of the tokens it uses.
"""

from enum import Enum

from chatette.parsing.line_count_file_wrapper impoprt LineCountFileWrapper

# Supported tokens
class Terminals(enum):
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


class Lexer(object):
    """
    This class is intended to manage the opening and reading of the template
    files and to transform the read stream of characters into
    a stream of tokens and additional information (terminal type).
    """
    def __init__(self):
        self._current_file = None
        self._opened_files = []
    
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
    

    def get_current_file_information(self):
        return (self._current_file.name, self._current_file.line_nb)
    def get_current_filename(self):
        return self._current_file.name
    


