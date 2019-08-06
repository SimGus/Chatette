# -*- coding: utf-8 -*-
"""
Module `chatette.refactor_parsing.lexing.rule_comment`
Contains the class representing the lexing rule that applies to comments.
"""

from chatette.refactor_parsing.lexing.lexing_rule import LexingRule
from chatette.refactor_parsing.lexing import LexicalToken, TerminalType
from chatette.refactor_parsing.utils import COMMENT_SYM, OLD_COMMENT_SYM


class RuleComment(LexingRule):
    def _apply_strategy(self):
        tokens = []
        text = self._text

        while self._next_index < len(text) and text[self._next_index].isspace():
            self._next_index += 1
        if self._next_index > self._start_index:
            matched_text = text[self._start_index:self._next_index]
            tokens.append(LexicalToken(TerminalType.whitespace, matched_text))
        if self._next_index >= len(text):
            return True
        
        if (   text.startswith(COMMENT_SYM, self._next_index)
            or text.startswith(OLD_COMMENT_SYM, self._next_index)
        ):
            matched_text = text[self._next_index:]
            tokens.append(LexicalToken(TerminalType.comment, matched_text))
            self._tokens = tokens
            self._next_index = len(text)
            return True

        # No comment found
        self.error_msg = \
            "Invalid token. Expected a comment there (starting with '" + \
            COMMENT_SYM + "' or '" + OLD_COMMENT_SYM + "')."
        return False
