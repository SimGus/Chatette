# coding: utf-8
"""
Module `chatette.refactor_parsing.lexing.rule_unit_ref`
Contains the definition of the class that represents the lexing rule
to tokenize a unit reference.
"""

from chatette.refactor_parsing.lexing.lexing_rule import LexingRule
from chatette.refactor_parsing.lexing import LexicalToken, TerminalType
from chatette.refactor_parsing.utils import \
    extract_identifier, \
    CASE_GEN_SYM, UNIT_END_SYM

from chatette.refactor_parsing.lexing.rule_unit_start import RuleUnitStart
from chatette.refactor_parsing.lexing.rule_variation import RuleVariation
from chatette.refactor_parsing.lexing.rule_rand_gen import RuleRandGen
from chatette.refactor_parsing.lexing.rule_arg_assignment import \
    RuleArgAssignment


class RuleUnitRef(LexingRule):
    def _apply_strategy(self, **kwargs):
        unit_start_rule = RuleUnitStart(self._text, self._next_index)
        if not unit_start_rule.matches(extracting_decl=False):
            self.error_msg = unit_start_rule.error_msg
            return False
        self._tokens.extend(unit_start_rule.get_lexical_tokens())
        self._next_index = unit_start_rule.get_next_index_to_match()
        
        if self._text.startswith(CASE_GEN_SYM, self._next_index):
            self._next_index += 1
            self._tokens.append(
                LexicalToken(TerminalType.casegen_mmarker, CASE_GEN_SYM)
            )

        identifier = extract_identifier(self._text, self._next_index)
        if identifier is not None:
            self._tokens.append(
                LexicalToken(TerminalType.unit_identifier, identifier)
            )
            self._next_index += len(identifier)
        
        if not self._match_any_order(
            [None, RuleVariation, RuleRandGen, RuleArgAssignment]
        ):
            return False
        
        if not self._text.startswith(UNIT_END_SYM, self._next_index):
            self.error_msg = \
                "Invalid token. Expected the unit reference to end here (" + \
                "using character '" + UNIT_END_SYM + "')."
            return False
        self._next_index += 1
        self._tokens.append(
            LexicalToken(TerminalType.unit_ref_end, UNIT_END_SYM)
        )
        
        return True
