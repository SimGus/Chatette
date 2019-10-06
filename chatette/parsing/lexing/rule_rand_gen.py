# coding: utf-8
"""
Module `chatette.parsing.lexing.rule_rand_gen`
Contains the definition of the class that represents the lexing rule
to tokenize a randgen modifier (inside a unit declaration, reference or
choice).
"""

from chatette.parsing.lexing.lexing_rule import LexingRule
from chatette.parsing.lexing import LexicalToken, TerminalType
from chatette.parsing.utils import \
    extract_identifier, \
    RAND_GEN_SYM, RAND_GEN_PERCENT_SYM, RAND_GEN_OPPOSITE_SYM

from chatette.parsing.lexing.rule_percent_gen import RulePercentGen


class RuleRandGen(LexingRule):
    def _apply_strategy(self, **kwargs):
        if not self._text.startswith(RAND_GEN_SYM, self._next_index):
            self.error_msg = \
                "Invalid token. Expected a random generation modifier to " + \
                "begin there (starting with '" + RAND_GEN_SYM + "')."
            return False
        self._next_index += 1
        self._update_furthest_matched_index()
        self._tokens.append(
            LexicalToken(TerminalType.randgen_marker, RAND_GEN_SYM)
        )

        if self._text.startswith(RAND_GEN_OPPOSITE_SYM, self._next_index):
            self._next_index += 1
            self._update_furthest_matched_index()
            self._tokens.append(
                LexicalToken(
                    TerminalType.opposite_randgen_marker, RAND_GEN_OPPOSITE_SYM
                )
            )

        # TODO not sure `extract_identifier` is the best thing to use here
        randgen_name = extract_identifier(self._text, self._next_index)
        if randgen_name is None:
            self.error_msg = \
                "Didn't expect the line to end there. Expected a name for " + \
                "the random generation modifier, a percentage for it or " + \
                "the end of the unit or choice."
            return False
        if len(randgen_name) > 0:
            self._next_index += len(randgen_name)
            self._update_furthest_matched_index()
            self._tokens.append(
                LexicalToken(TerminalType.randgen_name, randgen_name)
            )
        
        if self._text.startswith(RAND_GEN_PERCENT_SYM, self._next_index):
            self._next_index += 1
            self._update_furthest_matched_index()
            self._tokens.append(
                LexicalToken(
                    TerminalType.percentgen_marker, RAND_GEN_PERCENT_SYM
                )
            )

            if not self._try_to_match_rule(RulePercentGen):
                self.error_msg += \
                    " Percentage for the random generation is required after " + \
                    "its marker character ('" + RAND_GEN_PERCENT_SYM + "')."
                return False

        return True
