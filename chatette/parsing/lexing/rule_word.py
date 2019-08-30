# coding: utf-8
"""
Module `chatette.parsing.lexing.rule_word`
Contains the definition of the class that represents the lexing rule
to tokenize a word (inside a rule).
"""

from chatette.parsing.lexing.lexing_rule import LexingRule
from chatette.parsing.lexing import LexicalToken, TerminalType
from chatette.parsing.utils import \
    ESCAPEMENT_SYM, \
    FILE_INCLUSION_SYM, \
    UNIT_START_SYM, UNIT_END_SYM, \
    ALIAS_SYM, SLOT_SYM, INTENT_SYM, \
    SLOT_VAL_SYM, \
    CHOICE_START, CHOICE_END, CHOICE_SEP, \
    OLD_CHOICE_START, OLD_CHOICE_END, OLD_CHOICE_SEP, \
    RAND_GEN_SYM, \
    find_unescaped, find_next_comment
from chatette.utils import min_if_exist


class RuleWord(LexingRule):
    _should_be_escaped_chars = [
        FILE_INCLUSION_SYM,
        UNIT_START_SYM, UNIT_END_SYM,
        ALIAS_SYM, SLOT_SYM, INTENT_SYM,
        CHOICE_START, CHOICE_END, 
        OLD_CHOICE_START, OLD_CHOICE_END
    ]
    _should_be_escaped_in_choices_chars = [
        CHOICE_SEP,
        OLD_CHOICE_SEP,
        RAND_GEN_SYM
    ]
    _should_be_escaped_in_slot_def_chars = [SLOT_VAL_SYM]

    def _apply_strategy(self, **kwargs):
        """
        `kwargs` can contain a boolean with key `inside_choice` that is
        `True` when the current word is inside a choice and `False` otherwise.
        If this boolean is not in `kwargs`, defaults to `False`.
        ´kwargs´ can also contain a boolean with key `parsing_slot_def`
        which is `True` iff the current is in a rule inside a slot definition.
        If this boolean is not in `kwargs`, defaults to `False`.
        """
        inside_choice = kwargs.get("inside_choice", False)
        parsing_slot_def = kwargs.get("parsing_slot_def", False)

        # TODO this might be better using regexes
        if self._text[self._start_index].isspace():
            self.error_msg = \
                "Invalid token. Expected a word instead of a whitespace there."
            return False

        # Find whitespace after the word
        next_word_index = self._start_index + 1  # NOTE exclusive
        while True:
            if (
                next_word_index == len(self._text)
                or self._text[next_word_index].isspace()
            ):
                break
            next_word_index += 1
        
        next_word_index = \
            min_if_exist(
                next_word_index,
                find_next_comment(self._text, self._start_index)
            )

        if next_word_index == self._start_index:
            self.error_msg = "Invalid token. Expected a word to start here."
            return False
        for current_char in RuleWord._should_be_escaped_chars:
            if next_word_index == self._start_index:
                break
            next_word_index = \
                min_if_exist(
                    next_word_index,
                    find_unescaped(self._text, current_char, self._start_index)
                )
        
        if inside_choice and next_word_index > self._start_index:
            for char_to_escape in RuleWord._should_be_escaped_in_choices_chars:
                next_word_index = \
                    min_if_exist(
                        next_word_index,
                        find_unescaped(
                            self._text, char_to_escape, self._start_index
                        )
                    )
        
        if parsing_slot_def and next_word_index > self._start_index:
            for char_to_escape in RuleWord._should_be_escaped_in_slot_def_chars:
                next_word_index = \
                    min_if_exist(
                        next_word_index,
                        find_unescaped(
                            self._text, char_to_escape, self._start_index
                        )
                    )

        if next_word_index == self._start_index:
            self.error_msg = "Invalid token. Expected a word to start here."
            return False

        word = self._text[self._start_index:next_word_index]
        self._next_index = next_word_index
        self._update_furthest_matched_index()
        self._tokens.append(LexicalToken(TerminalType.word, word))
        return True
