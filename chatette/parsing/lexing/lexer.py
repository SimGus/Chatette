# -*- coding: utf-8 -*-
"""
Module `chatette.parsing`
Contains the lexer used by the parser and the definition of the tokens it uses.
"""

from chatette.parsing import utils as putils
from chatette.parsing.input_file_manager import InputFileManager
from chatette.parsing.lexing.rule_line import RuleLine


class Lexer(object):
    """
    This class is intended to transform each string it is provided
    into a "lexed" one, that is a list of dicts containing a label
    (the type of the terminal) and the token as a str.
    """
    def __init__(self):
        self._file_manager = InputFileManager.get_or_create()


    def lex(self, text, parsing_slot_def=False):
        """
        Returns a "lexed" version of the str `text`, that is
        a list of `LexedItem`s representing each token in `text`.
        Those `LexedItem`s contain a `TerminalType` representing
        the token's terminal type and a str with the token.
        `parsing_slot_def` should be `True` when `text` corresponds to
        the contents of a slot definition (its value for the slot declaration
        line is not important).
        """
        rule = RuleLine(text)
        if not rule.matches(parsing_slot_def=parsing_slot_def):
            rule.print_error()
        else:
            tokens = rule.get_lexical_tokens()
            for token in tokens:
                token.remove_escapement()
            return tokens
