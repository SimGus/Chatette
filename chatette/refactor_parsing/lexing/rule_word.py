# coding: utf-8
"""
Module `chatette.refactor_parsing.lexing.rule_word`
Contains the definition of the class that represents the lexing rule
to tokenize a word (inside a rule).
"""

from chatette.refactor_parsing.lexing.lexing_rule import LexingRule
from chatette.refactor_parsing.lexing import LexicalToken, TerminalType
from chatette.refactor_parsing.utils import \
    ESCAPEMENT_SYM, FILE_INCLUSION_SYM, UNIT_START_SYM, UNIT_END_SYM, \
    ALIAS_SYM, SLOT_SYM, INTENT_SYM, SLOT_VAL_SYM, CHOICE_START, CHOICE_END, \
    OLD_CHOICE_START, OLD_CHOICE_END, find_unescaped, find_next_comment
from chatette.utils import min_if_exist


class RuleWord(LexingRule):
    _should_be_escaped_chars = [
        FILE_INCLUSION_SYM,
        UNIT_START_SYM, UNIT_END_SYM,
        ALIAS_SYM, SLOT_SYM, INTENT_SYM,
        SLOT_VAL_SYM,
        CHOICE_START, CHOICE_END, OLD_CHOICE_START, OLD_CHOICE_END
    ]

    def _apply_strategy(self, **kwargs):
        # TODO this might be better using regexes
        # Find first whitespace
        end_word_index = self._start_index
        while True:
            if end_word_index == len(self._text):
                break
            if self._text[end_word_index].isspace():
                break
            end_word_index += 1
        
        end_word_index = \
            min_if_exist(
                end_word_index,
                find_next_comment(self, _text, self._start_index)
            )

        if end_word_index == self._start_index:
            self.error_msg = "Invalid token. Expected a word to start here."
            return False
        for current_char in RuleWord._should_be_escaped_chars:
            if end_word_index == self._start_index + 1:
                break
            end_word_index = \
                min_if_exist(
                    end_word_index,
                    find_unescaped(current_char, self._start_index)
                )

        word = self._text[self._start_index:end_word_index + 1]
        self._next_index = end_word_index + 1
        self._tokens.append(LexicalToken(TerminalType.word, word))
        return True
