# coding: utf-8
"""
Module `chatette.parsing.lexing.rule_unit_ref`
Contains the definition of the class that represents the lexing rule
to tokenize a unit reference.
"""

from chatette.parsing.lexing.lexing_rule import LexingRule
from chatette.parsing.lexing import LexicalToken, TerminalType
from chatette.parsing.utils import \
    extract_identifier, \
    CASE_GEN_SYM, UNIT_END_SYM

from chatette.parsing.lexing.rule_unit_start import RuleUnitStart
from chatette.parsing.lexing.rule_variation import RuleVariation
from chatette.parsing.lexing.rule_rand_gen import RuleRandGen
from chatette.parsing.lexing.rule_arg_assignment import \
    RuleArgAssignment


class RuleUnitRef(LexingRule):
    def _apply_strategy(self, **kwargs):
        unit_start_rule = RuleUnitStart(self._text, self._next_index)
        if not unit_start_rule.matches(extracting_decl=False):
            self.error_msg = unit_start_rule.error_msg
            self._update_furthest_matched_index(unit_start_rule)
            return False
        self._next_index = unit_start_rule.get_next_index_to_match()
        self._update_furthest_matched_index(unit_start_rule)
        self._tokens.extend(unit_start_rule.get_lexical_tokens())
        
        if self._text.startswith(CASE_GEN_SYM, self._next_index):
            self._tokens.append(
                LexicalToken(TerminalType.casegen_marker, CASE_GEN_SYM)
            )
            self._next_index += 1
            self._update_furthest_matched_index()

        identifier = extract_identifier(self._text, self._next_index)
        if identifier is not None:
            self._tokens.append(
                LexicalToken(TerminalType.unit_identifier, identifier)
            )
            self._next_index += len(identifier)
            self._update_furthest_matched_index()
        
        if not self._match_any_order(
            [None, RuleVariation, RuleRandGen, RuleArgAssignment]
        ):
            return False
        
        if not self._text.startswith(UNIT_END_SYM, self._next_index):
            self.error_msg = \
                "Invalid token. Expected the unit reference to end here (" + \
                "using character '" + UNIT_END_SYM + "')."
            return False

        # TODO maybe making a function for this would be useful
        if self._tokens[0].type == TerminalType.alias_ref_start:
            unit_end_type = TerminalType.alias_ref_end
        elif self._tokens[0].type == TerminalType.slot_ref_start:
            unit_end_type = TerminalType.slot_ref_end
        elif self._tokens[0].type == TerminalType.intent_ref_start:
            unit_end_type = TerminalType.intent_ref_end
        else:  # Should never happen
            raise ValueError(
                "An unexpected error happened during parsing: tried to " + \
                "parse the end of a unit but couldn't find its start in " + \
                "the previously parsed data.\nData was: " + str(self._tokens)
            )

        self._next_index += 1
        self._update_furthest_matched_index()
        self._tokens.append(LexicalToken(unit_end_type, UNIT_END_SYM))
        
        return True
