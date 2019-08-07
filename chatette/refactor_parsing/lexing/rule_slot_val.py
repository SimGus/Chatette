# coding: utf-8
"""
Module `chatette.refactor_parsing.lexing.rule_slot_val`
Contains the definition of the class that represents the lexing rule
to tokenize a slot value being set within a unit rule (only for a slot).
"""

from chatette.refactor_parsing.lexing.lexing_rule import LexingRule
from chatette.refactor_parsing.lexing import LexicalToken, TerminalType
from chatette.refactor_parsing.utils import find_next_comment, SLOT_VAL_SYM


class RuleSlotVal(LexingRule):
    def _apply_strategy(self):
        if slot_value_to_extract:  # TODO find how to get this info
            slot_value_tokens = []
            while self._text[index].isspace():
                self._next_index += 1

            if self._text.startswith(SLOT_VAL_SYM, index):
                slot_value_tokens.append(
                    LexicalToken(TerminalType.slot_val_marker, SLOT_VAL_SYM)
                )
                self._next_index += 1

                while self._text[index].isspace():
                    self._next_index += 1

                comment_sym = find_next_comment(self._text, self._next_index)
                if comment_sym is not None:
                    slot_value = \
                        self._text[self._next_index:comment_sym].rstrip()
                else:
                    slot_value = self._text[self._next_index:].rstrip()

                slot_value_tokens.append(
                    LexicalToken(TerminalType.slot_val, slot_value)
                )
                self._next_index += len(slot_value)

                return True
            else:
                return False
        else:
            raise ValueError(
                "Tried to extract a slot value within a rule that is not " + \
                "part of a slot definition."
            )
