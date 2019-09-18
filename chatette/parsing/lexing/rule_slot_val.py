# coding: utf-8
"""
Module `chatette.parsing.lexing.rule_slot_val`
Contains the definition of the class that represents the lexing rule
to tokenize a slot value being set within a unit rule (only for a slot).
"""

from chatette.parsing.lexing.lexing_rule import LexingRule
from chatette.parsing.lexing import LexicalToken, TerminalType
from chatette.parsing.utils import find_next_comment, SLOT_VAL_SYM


class RuleSlotVal(LexingRule):
    def _apply_strategy(self, **kwargs):
        """
        `kwargs` can contain a boolean with key `parsing_slot_def` that is
        `True` if the current text is part of a slot definition.
        If this boolean is not in `kwargs`, defaults to `False`.
        """
        parsing_slot_def = kwargs.get("parsing_slot_def", False)
        if parsing_slot_def:
            while self._text[self._next_index].isspace():
                self._next_index += 1
                self._update_furthest_matched_index()

            if self._text.startswith(SLOT_VAL_SYM, self._next_index):
                self._tokens.append(
                    LexicalToken(TerminalType.slot_val_marker, SLOT_VAL_SYM)
                )
                self._next_index += 1
                self._update_furthest_matched_index()

                while self._text[self._next_index].isspace():
                    self._next_index += 1
                    self._update_furthest_matched_index()

                comment_sym = find_next_comment(self._text, self._next_index)
                if comment_sym is not None:
                    slot_value = \
                        self._text[self._next_index:comment_sym].rstrip()
                else:
                    slot_value = self._text[self._next_index:].rstrip()

                self._tokens.append(
                    LexicalToken(TerminalType.slot_val, slot_value)
                )
                self._next_index += len(slot_value)
                self._update_furthest_matched_index()

                return True

            return False
        else:
            raise ValueError(
                "Tried to extract a slot value within a rule that is not " + \
                "part of a slot definition."
            )
