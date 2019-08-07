# coding: utf-8
"""
Module `chatette.refactor_parsing.lexing.rule_variation`
Contains the definition of the class that represents the lexing rule
to tokenize a variation (in a unit declaration or reference).
"""

from chatette.refactor_parsing.lexing.lexing_rule import LexingRule
from chatette.refactor_parsing.lexing import LexicalToken, TerminalType
from chatette.refactor_parsing.utils import VARIATION_SYM, extract_identifier


class RuleVariation(LexingRule):
    def _apply_strategy(self):
        if self._text.startswith(VARIATION_SYM, self._next_index):
            self._next_index += 1
            self._tokens.append(
                LexicalToken(TerminalType.variation_marker, VARIATION_SYM)
            )
        else:
            self.error_msg = \
                "Invalid token. Expected a variation there (starting with '" + \
                VARIATION_SYM + "')."
            return False
        
        variation_name = extract_identifier(self._text, self._next_index)
        if variation_name is None:
            self.error_msg = \
                "Didn't expect an end of line there. Expected a variation name."
            return False
        elif len(variation_name) == 0:
            self.error_msg = \
                "Couldn't extract the name of the variation. Variation names " + \
                "must be at least one character long."
            return False
        self._next_index += len(variation_name)
        self._tokens.append(
            LexicalToken(TerminalType.variation_name, variation_name)
        )
        return True
