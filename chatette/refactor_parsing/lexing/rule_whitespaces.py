# coding: utf-8
"""
Module `chatette.refactor_parsing.lexing.rule_whitespaces`
Contains the class representing the lexing rule that applies to whitespaces
and indentation.
"""

from chatette.refactor_parsing.lexing.lexing_rule import LexingRule
from chatette.refactor_parsing.lexing import LexicalToken, TerminalType


class RuleWhitespaces(LexingRule):
    def _apply_strategy(self):
        text = self._text

        while self._next_index < len(text) and text[self._next_index].isspace():
            self._next_index += 1
        if self._next_index > self._start_index:
            matched_text = text[self._start_index:self._next_index]
            self._tokens.append(
                LexicalToken(TerminalType.whitespace, matched_text)
            )
            return True
        
        self.error_msg = "Invalid token. Expected at least one whitespace there."
        return False
