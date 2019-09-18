# coding: utf-8
"""
Module `chatette.parsing.lexing.rule_comment`
Contains the class representing the lexing rule that applies to comments.
"""

from chatette.deprecations import Deprecations
from chatette.parsing.input_file_manager import InputFileManager

from chatette.parsing.lexing.lexing_rule import LexingRule
from chatette.parsing.lexing import LexicalToken, TerminalType
from chatette.parsing.utils import COMMENT_SYM, OLD_COMMENT_SYM

from chatette.parsing.lexing.rule_whitespaces import RuleWhitespaces


class RuleComment(LexingRule):
    def _apply_strategy(self, **kwargs):
        text = self._text

        whitespaces_rule = RuleWhitespaces(self._text, self._next_index)
        if whitespaces_rule.matches():
            self._next_index = whitespaces_rule.get_next_index_to_match()
            self._update_furthest_matched_index()
            # ignore the tokens it found since this whitespace is not meaningful
        if self._next_index >= len(text):
            return True
        
        if (   text.startswith(COMMENT_SYM, self._next_index)
            or text.startswith(OLD_COMMENT_SYM, self._next_index)
        ):
            if text.startswith(OLD_COMMENT_SYM, self._next_index):
                Deprecations.get_or_create().warn_old_comment(
                    *(InputFileManager \
                        .get_or_create() \
                        .get_current_line_information())
                )
            matched_text = text[self._next_index:]
            self._tokens.append(LexicalToken(TerminalType.comment, matched_text))
            self._next_index = len(text)
            self._update_furthest_matched_index()
            return True

        # No comment found
        self.error_msg = \
            "Invalid token. Expected a comment there (starting with '" + \
            COMMENT_SYM + "' or '" + OLD_COMMENT_SYM + "')."
        return False
