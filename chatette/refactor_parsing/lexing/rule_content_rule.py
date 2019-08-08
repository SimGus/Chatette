# coding: utf-8
"""
Module `chatette.refactor_parsing.lexing.rule_content_rule`
Contains the definition of the class that represents the lexing rule
to tokenize a line that is the contents of a rule inside a unit definition.
"""

from chatette.refactor_parsing.lexing.lexing_rule import LexingRule
from chatette.refactor_parsing.lexing import LexicalToken, TerminalType
from chatette.refactor_parsing.utils import find_next_comment, SLOT_VAL_SYM

from chatette.refactor_parsing.lexing.rule_whitespaces import RuleWhitespaces

class RuleContentRule(LexingRule):
    def _apply_strategy(self):
        if self._match_one_of(
            [RuleWord, RuleChoice, RuleUnitRef, RuleArgAssignment]
        ):
            if not self._try_to_match_rule(RuleWhitespaces):
                self.error_msg = None
        else:
            return False
