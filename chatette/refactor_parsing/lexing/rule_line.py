# -*- coding: utf-8 -*-
"""
Module `chatette.refactor_parsing.lexing.rule_line`
Contains the class representing a lexing rule that applies to a full line.
"""

from chatette.refactor_parsing.lexing.lexing_rule import LexingRule
from chatette.refactor_parsing.lexing.rule_comment import RuleComment


class RuleLine(LexingRule):
    """Represents the lexing rule for a full line of a template file."""
    def __init__(self, text):
        super(RuleLine, self).__init__(text, 0)
    
    def matches(self):
        if len(self._text.rstrip()) == 0:
            self._labelled_tokens = []
            self._matched = True
            return True
        
        comment_rule = RuleComment(self._text, 0)
        if comment_rule.matches():
            self._labelled_tokens = comment_rule.get_labelled_tokens()
            self._index = comment_rule.get_next_index()
            self._matched = True
        else:
            include_file_rule = RuleFileInclusion(self._text, 0)
            if include_file_rule.matches():
                self._labelled_tokens = include_file_rule.get_labelled_tokens()
                self._index = include_file_rule.get_next_index()
                self._matched = True
            else:
                unit_decl_line_rule = RuleUnitDeclLine(self._text, 0)
                if unit_decl_line_rule.matches():
                    self._labelled_tokens = \
                        unit_decl_line_rule.get_labelled_tokens()
                    self._index = unit_decl_line_rule.get_next_index()
                    self._matched = True
                else:
                    rule_line_rule = RuleLineRule(self._text, 0)
                    if rule_line_rule.matches():
                        self._labelled_tokens = \
                            rule_line_rule.get_labelled_tokens()
                        self._index = rule_line_rule.get_next_index()
                        self._matched = True
        
        if self._index < len(self._text):
            self._matched = False
            return False
        return True
        