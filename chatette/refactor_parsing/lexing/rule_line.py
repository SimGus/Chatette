# coding: utf-8
"""
Module `chatette.refactor_parsing.lexing.rule_line`
Contains the class representing a lexing rule that applies to a full line.
"""

from chatette.refactor_parsing.lexing.lexing_rule import LexingRule
from chatette.refactor_parsing.lexing.rule_comment import RuleComment
from chatette.refactor_parsing.lexing.rule_file_inclusion import \
    RuleFileInclusion
from chatette.refactor_parsing.lexing.rule_unit_decl_line import \
    RuleUnitDeclLine
from chatette.refactor_parsing.lexing.rule_unit_rule import RuleUnitRule


class RuleLine(LexingRule):
    """Represents the lexing rule for a full line of a template file."""
    _empty_match_allowed = True
    def __init__(self, text):
        super(RuleLine, self).__init__(text, 0)
    
    def _apply_strategy(self):
        if self._match_one_of(
            [RuleComment, RuleFileInclusion, RuleUnitDeclLine, RuleUnitRule]
        ):
            if self._next_index < len(self._text):
                comment_rule = RuleComment(
                    self._text, self._next_index
                )
                if comment_rule.matches():
                    self._tokens.extend(comment_rule.get_lexical_tokens())
                    self._next_index = comment_rule.get_next_index_to_match()
                    # Comments end the line BY DESIGN
                else:
                    self.error_msg = "Invalid token. Expected a comment or " + \
                        "the end of the line there."
            return True
        return False
    