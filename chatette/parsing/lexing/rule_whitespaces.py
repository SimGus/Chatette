# coding: utf-8
"""
Module `chatette.parsing.lexing.rule_whitespaces`
Contains the class representing the lexing rule that applies to whitespaces
and indentation.
"""

from chatette.parsing.lexing.lexing_rule import LexingRule
from chatette.parsing.lexing import LexicalToken, TerminalType


class RuleWhitespaces(LexingRule):
    def _apply_strategy(self, **kwargs):
        """
        `kwargs` can contain a boolean at key `parsing_indentation` that is
        `True` iff the whitespaces currently parsed correspond to
        an indentation, and `False` if it corresponds to simple whitespaces.
        If `kwargs` doesn't contain this boolean, defaults to `False`.
        """
        parsing_indentation = kwargs.get("parsing_indentation", False)
        if parsing_indentation:
            terminal_type = TerminalType.indentation
        else:
            terminal_type = TerminalType.whitespace
        text = self._text

        while self._next_index < len(text) and text[self._next_index].isspace():
            self._next_index += 1
            self._update_furthest_matched_index()
        if self._next_index > self._start_index:
            matched_text = text[self._start_index:self._next_index]
            self._tokens.append(LexicalToken(terminal_type, matched_text))
            return True
        
        self.error_msg = "Invalid token. Expected at least one whitespace there."
        return False
