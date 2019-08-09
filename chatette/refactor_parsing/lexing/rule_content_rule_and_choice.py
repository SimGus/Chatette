# coding: utf-8
"""
Module `chatette.refactor_parsing.lexing.rule_content_rule_and_choice`
Contains the definition of the class that represents the lexing rule
to tokenize a line that is the contents of a rule inside a unit definition,
and the definition of the class that represents the lexing rule
to tokenize a choice (inside the contents of a rule).
Both classes are defined here to prevent circular imports (cf. below).
"""

from chatette.refactor_parsing.lexing.lexing_rule import LexingRule
from chatette.refactor_parsing.lexing import LexicalToken, TerminalType
from chatette.refactor_parsing.utils import find_next_comment, \
    SLOT_VAL_SYM, \
    OLD_CHOICE_START, OLD_CHOICE_END, OLD_CHOICE_SEP, \
    CASE_GEN_SYM

from chatette.refactor_parsing.lexing.rule_word import RuleWord
from chatette.refactor_parsing.lexing.rule_unit_ref import RuleUnitRef
from chatette.refactor_parsing.lexing.rule_arg_assignment import \
    RuleArgAssignment
from chatette.refactor_parsing.lexing.rule_whitespaces import RuleWhitespaces
from chatette.refactor_parsing.lexing.rule_rand_gen import RuleRandGen


class RuleContentRule(LexingRule):
    def _apply_strategy(self, **kwargs):
        if self._match_one_of(
            [RuleWord, RuleChoice, RuleUnitRef, RuleArgAssignment],
            self._next_index,
            **kwargs
        ):
            if not self._try_to_match_rule(RuleWhitespaces):
                self.error_msg = None
            return True
        else:
            return False

# NOTE Required to put it here rather than in its own module 
#      to prevent circular imports.
#      Indeed, instances of `RuleContentRule` can contain instances of
#      `RuleChoice`, which in turn can contain instances of `RuleContentRule`.
class RuleChoice(LexingRule):
    def _apply_strategy(self, **kwargs):
        if not self._text.startswith(OLD_CHOICE_START, self._next_index):
            self.error_msg = \
                "Invalid token. Expected a choice to start there (starting " + \
                "with '" + OLD_CHOICE_START + "')."
            return False
        self._next_index += 1
        self._tokens.append(
            LexicalToken(TerminalType.choice_start, OLD_CHOICE_START)
        )

        if self._text.startswith(CASE_GEN_SYM, self._next_index):
            self._next_index += 1
            self._tokens.append(
                LexicalToken(TerminalType.casegen_marker, CASE_GEN_SYM)
            )

        if not self._try_to_match_rule(RuleWhitespaces):
            self.error_msg = None

        while True:
            if self._text.startswith(OLD_CHOICE_SEP, self._next_index):
                self._next_index += 1
                self._tokens.append(
                    LexicalToken(TerminalType.choice_sep, OLD_CHOICE_SEP)
                )
                if not self._try_to_match_rule(RuleWhitespaces):
                    self.error_msg = None

            rule_content_rule = RuleContentRule(self._text, self._next_index)
            if not rule_content_rule.matches(inside_rule=True):
                self.error_msg = None
                break
            self._next_index = rule_content_rule.get_next_index_to_match()
            self._tokens.extend(rule_content_rule.get_lexical_tokens())
        
        if not self._try_to_match_rule(RuleRandGen):
            self.error_msg = None
        
        if not self._text.startswith(OLD_CHOICE_END, self._next_index):
            self.error_msg = \
                "Invalid token. Expected the choice to end here (using " + \
                "character '" + OLD_CHOICE_END + "')."
            return False
        self._next_index += 1
        self._tokens.append(
            LexicalToken(TerminalType.choice_end,OLD_CHOICE_END)
        )