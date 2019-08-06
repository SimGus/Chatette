# -*- coding: utf-8 -*-
"""
Module `chatette.refactor_parsing.lexing.rule_comment`
Contains the class representing the lexing rule that applies to comments.
"""

from chatette.refactor_parsing.lexing.lexing_rule import LexingRule
from chatette.refactor_parsing.lexing import LexicalToken, TerminalType


class RuleComment(LexingRule):
    def matches(self):
        labelled_tokens = []
        text = self._text

        index = self._index
        while index < len(text) and text[index].isspace():
            index += 1
        if index > self._index:
            labelled_tokens.append(
                LexicalToken(TerminalType.whitespace, text[self._index:index])
            )

        if text.startswith('//', index):
            self._matched = True
            labelled_tokens.append(
                LexicalToken(TerminalType.comment, text[index:])
            )
            self._labelled_tokens = labelled_tokens
            self._next_index = len(text)
            return True
        self._matched = False
        return False
