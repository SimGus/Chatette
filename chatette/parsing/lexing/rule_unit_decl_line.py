# coding: utf-8
"""
Module `chatette.parsing.lexing.rule_unit_decl_line`
Contains the definition of the class that represents the lexing rule
to tokenize a line that declares a unit.
"""

from chatette.parsing.lexing.lexing_rule import LexingRule
from chatette.parsing.lexing import LexicalToken, TerminalType
from chatette.parsing.utils import CASE_GEN_SYM, UNIT_END_SYM

from chatette.parsing.lexing.rule_unit_decl import RuleUnitDecl
from chatette.parsing.lexing.rule_annotation import RuleAnnotation


class RuleUnitDeclLine(LexingRule):
    def _apply_strategy(self, **kwargs):
        if not self._try_to_match_rule(RuleUnitDecl):
            return False
        
        annotation_rule = RuleAnnotation(self._text, self._next_index)
        if annotation_rule.matches():
            self._next_index = annotation_rule.get_next_index_to_match()
            self._update_furthest_matched_index()
            self._tokens.extend(annotation_rule.get_lexical_tokens())
        return True
