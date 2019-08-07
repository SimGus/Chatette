# coding: utf-8
"""
Module `chatette.refactor_parsing.lexing.rule_unit_decl`
Contains the definition of the class that represents the lexing rule
to tokenize a line that declares a unit.
"""

from chatette.refactor_parsing.lexing.lexing_rule import LexingRule
from chatette.refactor_parsing.lexing import LexicalToken, TerminalType
from chatette.refactor_parsing.utils import CASE_GEN_SYM, UNIT_END_SYM


class RuleUnitDeclLine(LexingRule):
    def _apply_strategy(self):
        if not self._try_to_match_rule(RuleUnitDecl):
            return False
        
        annotation_rule = RuleAnnotation(self._text, self._next_index)
        if annotation_rule.matches():
            self._tokens.append(annotation_rule.get_lexical_tokens())
            self._next_index = annotation_rule.get_next_index_to_match()
        return True
