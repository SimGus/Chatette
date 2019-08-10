# coding: utf-8
"""
Module `chatette.refactor_parsing.lexing.rule_unit_rule`
Contains the definition of the class that represents the lexing rule
to tokenize a rule that is part of a unit definition.
"""

from chatette.refactor_parsing.lexing.lexing_rule import LexingRule
from chatette.refactor_parsing.lexing import LexicalToken, TerminalType
from chatette.refactor_parsing.utils import find_next_comment, SLOT_VAL_SYM

from chatette.refactor_parsing.lexing.rule_whitespaces import RuleWhitespaces
from chatette.refactor_parsing.lexing.rule_content_rule_and_choice import \
    RuleContentRule
from chatette.refactor_parsing.lexing.rule_comment import RuleComment


class RuleUnitRule(LexingRule):
    def _apply_strategy(self, **kwargs):
        """
        `kwargs` can contain a boolean with key `parsing_slot_def` that is
        `True` if the current text is part of a slot definition.
        If this boolean is not in `kwargs`, defaults to `False`.
        """
        parsing_slot_def = kwargs.get("parsing_slot_def", False)

        if not self._try_to_match_rule(RuleWhitespaces):
            self.error_msg = \
                "Invalid token. Expected indentation within unit definitions."
            return False
        
        while True:
            if self._next_index == len(self._text):
                return True
            content_rule = RuleContentRule(self._text, self._next_index)
            if content_rule.matches():
                self._tokens.extend(content_rule.get_lexical_tokens())
                self._next_index = content_rule.get_next_index_to_match()
                self._update_furthest_matched_index(content_rule)
            else:
                break
        
        if parsing_slot_def:
            if not self._try_to_match_rule(RuleSlotVal):
                self.error_msg = None
        
        if self._next_index < len(self._text):
            self._try_to_match_rule(RuleComment)
        
        if self._next_index < len(self._text):
            return False
        return True
