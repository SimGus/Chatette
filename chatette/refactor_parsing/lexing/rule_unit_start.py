# coding: utf-8
"""
Module `chatette.refactor_parsing.lexing.rule_unit_start`
Contains the class that represents a lexing rule to tokenize
the start of a unit definition or reference.
"""

from chatette.refactor_parsing.lexing.lexing_rule import LexingRule
from chatette.refactor_parsing.lexing import LexicalToken, TerminalType
from chatette.refactor_parsing.utils import \
    ALIAS_SYM, SLOT_SYM, INTENT_SYM, UNIT_START_SYM


class RuleUnitStart(LexingRule):
    def _apply_strategy(self):
        if self._text.startswith(ALIAS_SYM, self._next_index):
            terminal_type = TerminalType.alias_decl_start
            text_start = ALIAS_SYM
        elif self._text.startswith(SLOT_SYM, self._next_index):
            terminal_type = TerminalType.slot_decl_start
            text_start = SLOT_SYM
        elif self._text.startswith(INTENT_SYM, self._next_index):
            terminal_type = TerminalType.intent_decl_start
            text_start = INTENT_SYM
        else:
            self.error_msg = \
                "Invalid token. Expected a unit start here (starting with " + \
                "either '" + ALIAS_SYM + "', '" + SLOT_SYM + "' or '" + \
                INTENT_SYM + "'."
            return False
        self._next_index += 1

        if self._text.startswith(UNIT_START_SYM, self._next_index):
            self._tokens.append(
                LexicalToken(terminal_type, text_start + UNIT_START_SYM)
            )
            self._next_index += 1
            return True
        
        self.error_msg = \
            "Invalid token. Expected a start of unit here (starting with '" + \
            UNIT_START_SYM + "'). Did you mean to escape the previous '" + \
            text_start + '?'
        return False
