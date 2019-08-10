# coding: utf-8
"""
Module `chatette.refactor_parsing.lexing.rule_arg_assignment`
Contains the class representing the lexing rule meant to tokenize
an argument assignment (inside a unit reference).
"""

from chatette.refactor_parsing.lexing.lexing_rule import LexingRule
from chatette.refactor_parsing.lexing import LexicalToken, TerminalType
from chatette.refactor_parsing.utils import ARG_SYM, extract_identifier


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

        arg_name = extract_identifier(self._text, self._next_index)
        if arg_name is None:
            self.error_msg = \
                "Didn't expect the line to end there. Expected an argument name."
            return False
        elif len(arg_name) == 0:
            self.error_msg = \
                "Couldn't extract the argument name. Arguments must have a name."
            return False
        self._next_index += len(arg_name)
        self._update_furthest_matched_index()
        self._tokens.append(
            LexicalToken(TerminalType.arg_name, arg_name)
        )
        return True
