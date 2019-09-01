# coding: utf-8
"""
Module `chatette.parsing.lexing.rule_unit_rule`
Contains the definition of the class that represents the lexing rule
to tokenize a rule that is part of a unit definition.
"""

from chatette.parsing.lexing.lexing_rule import LexingRule
from chatette.parsing.lexing import LexicalToken, TerminalType
from chatette.parsing.utils import find_next_comment, SLOT_VAL_SYM

from chatette.parsing.lexing.rule_whitespaces import RuleWhitespaces
from chatette.parsing.lexing.rule_content_rule_and_choice import \
    RuleContentRule
from chatette.parsing.lexing.rule_comment import RuleComment
from chatette.parsing.lexing.rule_slot_val import RuleSlotVal


class RuleUnitRule(LexingRule):
    def _apply_strategy(self, **kwargs):
        """
        `kwargs` can contain a boolean with key `parsing_slot_def` that is
        `True` if the current text is part of a slot definition.
        If this boolean is not in `kwargs`, defaults to `False`.
        """
        parsing_slot_def = kwargs.get("parsing_slot_def", False)

        if not self._try_to_match_rule(
            RuleWhitespaces, parsing_indentation=True
        ):
            self.error_msg = \
                "Invalid token. Expected indentation within unit definitions."
            return False
        
        while True:
            if self._next_index == len(self._text):
                return True
            content_rule = RuleContentRule(self._text, self._next_index)
            if content_rule.matches(**kwargs):
                self._tokens.extend(content_rule.get_lexical_tokens())
                self._next_index = content_rule.get_next_index_to_match()
                self._update_furthest_matched_index(content_rule)
            else:
                self._update_furthest_matched_index(content_rule)
                self.error_msg = content_rule.error_msg
                break
        
        if parsing_slot_def:
            old_error_msg = self.error_msg
            if not self._try_to_match_rule(RuleSlotVal, **kwargs):
                self.error_msg = old_error_msg
        
        if self._next_index < len(self._text):
            old_error_msg = self.error_msg
            if (
                not self._try_to_match_rule(RuleComment) and old_error_msg is not None
            ):
                self.error_msg = old_error_msg
        
        if self._next_index < len(self._text):
            return False
        return True
