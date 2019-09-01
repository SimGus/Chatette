# coding: utf-8
"""
Module `chatette.parsing.lexing.rule_line`
Contains the class representing a lexing rule that applies to a full line.
"""

from chatette.parsing.lexing.lexing_rule import LexingRule
from chatette.parsing.lexing.rule_comment import RuleComment
from chatette.parsing.lexing.rule_file_inclusion import \
    RuleFileInclusion
from chatette.parsing.lexing.rule_unit_decl_line import \
    RuleUnitDeclLine
from chatette.parsing.lexing.rule_unit_rule import RuleUnitRule


class RuleLine(LexingRule):
    """Represents the lexing rule for a full line of a template file."""
    _empty_match_allowed = True
    def __init__(self, text):
        super(RuleLine, self).__init__(text, 0)
    
    def _apply_strategy(self, **kwargs):
        if self._match_one_of(
            [RuleComment, RuleFileInclusion, RuleUnitDeclLine, RuleUnitRule],
            self._next_index,
            **kwargs
        ):
            if self._next_index < len(self._text):
                comment_rule = RuleComment(self._text, self._next_index)
                if not comment_rule.matches():
                    self.error_msg = "Invalid token. Expected a comment or " + \
                        "the end of the line there."
                    self._update_furthest_matched_index(comment_rule)
                    return False
                self._tokens.extend(comment_rule.get_lexical_tokens())
                self._next_index = comment_rule.get_next_index_to_match()
                self._update_furthest_matched_index()
                # Comments end the line BY DESIGN
                return True

            return True

        return False
    