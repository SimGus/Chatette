# coding: utf-8
"""
Module `chatette.parsing.lexing.rule_file_inclusion`
Contains the definition of the class that represents the lexing rule
that has to do with a line that includes a file.
"""

from chatette.parsing.lexing.lexing_rule import LexingRule
from chatette.parsing.lexing import LexicalToken, TerminalType
from chatette.parsing.utils import \
    FILE_INCLUSION_SYM, COMMENT_SYM, OLD_COMMENT_SYM, find_next_comment
from chatette.utils import min_if_exist


class RuleFileInclusion(LexingRule):
    def _apply_strategy(self, **kwargs):
        if not self._text.startswith(FILE_INCLUSION_SYM, self._next_index):
            self.error_msg = \
                "Invalid token. Expected a file to be included there " + \
                "(starting with '" + FILE_INCLUSION_SYM + "')."
            return False
        self._next_index += 1
        self._update_furthest_matched_index()
        self._tokens.append(
            LexicalToken(
                TerminalType.file_inclusion_marker, FILE_INCLUSION_SYM
            )
        )

        if self._text[self._next_index].isspace():
            self.error_msg = \
                "Invalid token. Expected a file path here, got a whitespace."
            return False
        
        comment_start = find_next_comment(self._text, self._next_index)
        if comment_start is not None:
            file_path = self._text[self._next_index:comment_start].rstrip()
        else:
            file_path = self._text[self._next_index:].rstrip()

        self._next_index += len(file_path)
        self._update_furthest_matched_index()
        self._tokens.append(LexicalToken(TerminalType.file_path, file_path))

        return True
