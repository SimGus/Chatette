# coding: utf-8
"""
Module `chatette.parsing.lexing.rule_percent_gen`
Contains the class representing the lexing rule meant to tokenize
percentage for the random generation modifiers.
"""

from chatette.parsing.lexing.lexing_rule import LexingRule
from chatette.parsing.lexing import LexicalToken, TerminalType

from chatette.parsing.lexing.rule_whitespaces import RuleWhitespaces


class RulePercentGen(LexingRule):
    def _apply_strategy(self, **kwargs):
        while self._text[self._next_index].isdigit():
            self._next_index += 1
            self._update_furthest_matched_index()
        percentage = self._text[self._start_index:self._next_index]

        if self._text[self._next_index] != '.':
            if len(percentage) == 0:
                self.error_msg = \
                    "Invalid token. Expected a percentage for the random " + \
                    "generation modifier."
                return False
        else:
            percentage += '.'
            self._next_index += 1
            self._update_furthest_matched_index()

            start_index_non_int_part = self._next_index
            while self._text[self._next_index].isdigit():
                self._next_index += 1
                self._update_furthest_matched_index()
            if self._next_index == start_index_non_int_part:
                self.error_msg = \
                    "Invalid token. Cannot have a percentage with an empty " + \
                    "non-integral part."
                return False
            percentage += self._text[start_index_non_int_part:self._next_index]
            
        if not self._try_to_match_rule(RuleWhitespaces):
            self.error_msg = None
            # Ignore tokens as this whitespace is not meaningful
        if self._text[self._next_index] == '%':
            self._next_index += 1
            self._update_furthest_matched_index()
        
        self._tokens.append(LexicalToken(TerminalType.percentgen, percentage))

        return True
