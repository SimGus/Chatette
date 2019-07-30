"""
Module `chatette.refactor_parsing`
Contains the lexer used by the parser and the definition of the tokens it uses.
"""

from enum import Enum

from chatette.refactor_parsing.input_file_manager import InputFileManager


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
    This class is intended to transform each string it is provided
    into a "lexed" one, that is a list of dicts containing a label
    (the type of the terminal) and the token as a str.
    """
    def __init__(self):
        self._file_manager = InputFileManager.get_or_create()

    def lex(self, text):
        """
        Returns a "lexed" version of the str `text`, that is
        a list of dicts representing each token in `text`.
        Those dicts contain a `TerminalType` representing
        the token's terminal type and a str with the token,
        and this in the following format:
        `{"token-type": TerminalType, "token": str}`.
        """
        if len(text) == 0:
            return []
        current_index = 0
        lexed_text = []

        # TODO

        return lexed_text
