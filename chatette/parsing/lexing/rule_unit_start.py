# coding: utf-8
"""
Module `chatette.parsing.lexing.rule_unit_start`
Contains the class that represents a lexing rule to tokenize
the start of a unit definition or reference.
"""

from chatette.parsing.lexing.lexing_rule import LexingRule
from chatette.parsing.lexing import LexicalToken, TerminalType
from chatette.parsing.utils import \
    ALIAS_SYM, SLOT_SYM, INTENT_SYM, UNIT_START_SYM


class RuleUnitStart(LexingRule):
    def _apply_strategy(self, **kwargs):
        """
        `kwargs` can contain a value with key `extracting_decl`.
        This is a boolean that should be `True` iff the rule should consider
        it is parsing a unit declaration and `False` if it is parsing
        a unit reference.
        If `kwargs` doesn't contain `extracting_decl`, defaults to `True`.
        """
        extracting_decl = kwargs.get("extracting_decl", True)
        if self._text.startswith(ALIAS_SYM, self._next_index):
            if extracting_decl:
                terminal_type = TerminalType.alias_decl_start
            else:
                terminal_type = TerminalType.alias_ref_start
            text_start = ALIAS_SYM
        elif self._text.startswith(SLOT_SYM, self._next_index):
            if extracting_decl:
                terminal_type = TerminalType.slot_decl_start
            else:
                terminal_type = TerminalType.slot_ref_start
            text_start = SLOT_SYM
        elif self._text.startswith(INTENT_SYM, self._next_index):
            if extracting_decl:
                terminal_type = TerminalType.intent_decl_start
            else:
                terminal_type = TerminalType.intent_ref_start
            text_start = INTENT_SYM
        else:
            self.error_msg = \
                "Invalid token. Expected a unit start here (starting with " + \
                "either '" + ALIAS_SYM + "', '" + SLOT_SYM + "' or '" + \
                INTENT_SYM + "'."
            return False
        self._next_index += 1
        self._update_furthest_matched_index()

        if self._text.startswith(UNIT_START_SYM, self._next_index):
            self._tokens.append(
                LexicalToken(terminal_type, text_start + UNIT_START_SYM)
            )
            self._next_index += 1
            self._update_furthest_matched_index()
            return True
        
        self.error_msg = \
            "Invalid token. Expected a start of unit here (starting with '" + \
            UNIT_START_SYM + "'). Did you mean to escape the previous '" + \
            text_start + '?'
        return False
