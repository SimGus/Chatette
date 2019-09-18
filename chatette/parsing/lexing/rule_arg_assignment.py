# coding: utf-8
"""
Module `chatette.parsing.lexing.rule_arg_assignment`
Contains the class representing the lexing rule meant to tokenize
an argument assignment (inside a unit reference).
"""

from chatette.parsing.lexing.lexing_rule import LexingRule
from chatette.parsing.lexing import LexicalToken, TerminalType
from chatette.parsing.utils import ARG_SYM, extract_identifier


class RuleArgAssignment(LexingRule):
    def _apply_strategy(self, **kwargs):
        if not self._text.startswith(ARG_SYM, self._next_index):
            self.error_msg = \
                "Invalid token. Expected an argument assignment to start " + \
                "here (starting with '" + ARG_SYM + "')."
            return False
        self._next_index += 1
        self._update_furthest_matched_index()
        self._tokens.append(LexicalToken(TerminalType.arg_marker, ARG_SYM))

        arg_value = extract_identifier(self._text, self._next_index)
        if arg_value is None:
            self.error_msg = \
                "Didn't expect the line to end there. Expected an argument name."
            return False
        elif len(arg_value) == 0:
            self.error_msg = \
                "Couldn't extract the argument name. Arguments must have a name."
            return False
        self._next_index += len(arg_value)
        self._update_furthest_matched_index()
        self._tokens.append(
            LexicalToken(TerminalType.arg_value, arg_value)
        )
        return True
