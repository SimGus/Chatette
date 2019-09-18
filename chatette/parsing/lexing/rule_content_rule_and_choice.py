# coding: utf-8
"""
Module `chatette.parsing.lexing.rule_content_rule_and_choice`
Contains the definition of the class that represents the lexing rule
to tokenize a line that is the contents of a rule inside a unit definition,
and the definition of the class that represents the lexing rule
to tokenize a choice (inside the contents of a rule).
Both classes are defined here to prevent circular imports (cf. below).
"""

from chatette.deprecations import Deprecations
from chatette.parsing.input_file_manager import InputFileManager

from chatette.parsing.lexing.lexing_rule import LexingRule
from chatette.parsing.lexing import LexicalToken, TerminalType
from chatette.parsing.utils import find_next_comment, \
    SLOT_VAL_SYM, \
    CHOICE_START, CHOICE_END, CHOICE_SEP, \
    OLD_CHOICE_START, OLD_CHOICE_END, OLD_CHOICE_SEP, \
    CASE_GEN_SYM

from chatette.parsing.lexing.rule_word import RuleWord
from chatette.parsing.lexing.rule_unit_ref import RuleUnitRef
from chatette.parsing.lexing.rule_arg_assignment import \
    RuleArgAssignment
from chatette.parsing.lexing.rule_whitespaces import RuleWhitespaces
from chatette.parsing.lexing.rule_rand_gen import RuleRandGen


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

        return False

# NOTE Required to put it here rather than in its own module 
#      to prevent circular imports.
#      Indeed, instances of `RuleContentRule` can contain instances of
#      `RuleChoice`, which in turn can contain instances of `RuleContentRule`.
class RuleChoice(LexingRule):
    def _apply_strategy(self, **kwargs):
        start_char = None
        if self._text.startswith(OLD_CHOICE_START, self._next_index):
            start_char = OLD_CHOICE_START
            sep_char = OLD_CHOICE_SEP
            end_char = OLD_CHOICE_END
            Deprecations.get_or_create().warn_old_choice(
                *(InputFileManager \
                    .get_or_create() \
                    .get_current_line_information())
            )
        elif self._text.startswith(CHOICE_START, self._next_index):
            start_char = CHOICE_START
            sep_char = CHOICE_SEP
            end_char = CHOICE_END
        
        if start_char is None:
            self.error_msg = \
                "Invalid token. Expected a choice to start there (starting " + \
                "with '" + CHOICE_START + "' or '" + OLD_CHOICE_START + "')."
            return False
        self._next_index += 1
        self._update_furthest_matched_index()
        self._tokens.append(
            LexicalToken(TerminalType.choice_start, start_char)
        )

        if self._text.startswith(CASE_GEN_SYM, self._next_index):
            self._next_index += 1
            self._update_furthest_matched_index()
            self._tokens.append(
                LexicalToken(TerminalType.casegen_marker, CASE_GEN_SYM)
            )

        if not self._try_to_match_rule(RuleWhitespaces):
            self.error_msg = None

        while True:
            if self._text.startswith(sep_char, self._next_index):
                self._next_index += 1
                self._update_furthest_matched_index()
                self._tokens.append(
                    LexicalToken(TerminalType.choice_sep, sep_char)
                )
                if not self._try_to_match_rule(RuleWhitespaces):
                    self.error_msg = None

            rule_content_rule = RuleContentRule(self._text, self._next_index)
            if not rule_content_rule.matches(inside_choice=True):
                self.error_msg = None
                self._update_furthest_matched_index(rule_content_rule)
                break
            self._next_index = rule_content_rule.get_next_index_to_match()
            self._update_furthest_matched_index(rule_content_rule)
            self._tokens.extend(rule_content_rule.get_lexical_tokens())
        
        if not self._try_to_match_rule(RuleRandGen):
            self.error_msg = None
        
        if not self._text.startswith(end_char, self._next_index):
            self.error_msg = \
                "Invalid token. Unmatched choice opening character. " + \
                "Expected the choice to end here (using " + \
                "character '" + end_char + "')."
            return False
        self._next_index += 1
        self._update_furthest_matched_index()
        self._tokens.append(LexicalToken(TerminalType.choice_end, end_char))

        return True