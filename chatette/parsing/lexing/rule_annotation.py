# coding: utf-8
"""
Module `chatette.parsing.lexing.rule_annotation`
Contains the definition of the class that represents the lexing rule
to tokenize an annotation (binded to an intent definition).
"""

from chatette.parsing.lexing.lexing_rule import LexingRule
from chatette.parsing.lexing import LexicalToken, TerminalType
from chatette.parsing.utils import \
    ANNOTATION_START, ANNOTATION_END, ANNOTATION_SEP, KEY_VAL_CONNECTOR

from chatette.parsing.lexing.rule_whitespaces import RuleWhitespaces
from chatette.parsing.lexing.rule_key_value import RuleKeyValue


class RuleAnnotation(LexingRule):
    def _apply_strategy(self, **kwargs):
        if self._text.startswith(ANNOTATION_START, self._next_index):
            self._next_index += 1
            self._update_furthest_matched_index()
            self._tokens.append(
                LexicalToken(TerminalType.annotation_start, ANNOTATION_START)
            )
        else:
            self.error_msg = \
                "Invalid token. Expected an annotation there (starting with '" + \
                ANNOTATION_START + "')."
            return False
        
        whitespaces_rule = RuleWhitespaces(self._text, self._next_index)
        if whitespaces_rule.matches():
            self._next_index = whitespaces_rule.get_next_index_to_match()
            self._update_furthest_matched_index(whitespaces_rule)
            # Ignoring the tokens because whitespaces here are not meaningful
        
        # Empty annotation
        if self._text.startswith(ANNOTATION_END, self._next_index):
            self._next_index += 1
            self._update_furthest_matched_index()
            self._tokens.append(
                LexicalToken(TerminalType.annotation_end, ANNOTATION_END)
            )
            return True

        first_key_val_rule = RuleKeyValue(self._text, self._next_index)
        if not first_key_val_rule.matches():
            self.error_msg = first_key_val_rule.error_msg
            self._update_furthest_matched_index(first_key_val_rule)
            return False
        self._tokens.extend(first_key_val_rule.get_lexical_tokens())
        self._update_furthest_matched_index(first_key_val_rule)
        self._next_index = first_key_val_rule.get_next_index_to_match()

        whitespaces_rule = RuleWhitespaces(self._text, self._next_index)
        if whitespaces_rule.matches():
            self._next_index = whitespaces_rule.get_next_index_to_match()
            self._update_furthest_matched_index()
            # Ignoring the tokens because whitespaces here are not meaningful

        if not self._text.startswith(KEY_VAL_CONNECTOR, self._next_index):
            # Single value
            self._tokens[-1].type = TerminalType.value
        else:
            # Multiple key/value pairs
            self._next_index += 1
            self._update_furthest_matched_index()
            self._tokens.append(
                LexicalToken(
                    TerminalType.key_value_connector, KEY_VAL_CONNECTOR
                )
            )

            whitespaces_rule = RuleWhitespaces(self._text, self._next_index)
            if whitespaces_rule.matches():
                self._next_index = whitespaces_rule.get_next_index_to_match()
                self._update_furthest_matched_index()
                # Ignoring the tokens because whitespaces here are not meaningful

            first_val_rule = RuleKeyValue(self._text, self._next_index)
            if not first_val_rule.matches(extracting_key=False):
                self.error_msg = first_val_rule.error_msg
                self._update_furthest_matched_index(first_val_rule)
                return False
            
            self._next_index = first_val_rule.get_next_index_to_match()
            self._update_furthest_matched_index(first_val_rule)
            self._tokens.extend(first_val_rule.get_lexical_tokens())

            whitespaces_rule = RuleWhitespaces(self._text, self._next_index)
            if whitespaces_rule.matches():
                self._next_index = whitespaces_rule.get_next_index_to_match()
                self._update_furthest_matched_index()
                # Ignoring the tokens because whitespaces here are not meaningful
            
            while self._text.startswith(ANNOTATION_SEP, self._next_index):
                self._next_index += 1
                self._update_furthest_matched_index()
                self._tokens.append(
                    LexicalToken(TerminalType.separator, ANNOTATION_SEP)
                )

                whitespaces_rule = RuleWhitespaces(self._text, self._next_index)
                if whitespaces_rule.matches():
                    self._next_index = whitespaces_rule.get_next_index_to_match()
                    self._update_furthest_matched_index()
                    # Ignoring the tokens because whitespaces here are not meaningful

                key_rule = RuleKeyValue(self._text, self._next_index)
                if not key_rule.matches(extracting_key=True):
                    self.error_msg = key_rule.error_msg
                    self._update_furthest_matched_index(key_rule)
                    return False
                self._next_index = key_rule.get_next_index_to_match()
                self._update_furthest_matched_index(key_rule)
                self._tokens.extend(key_rule.get_lexical_tokens())

                whitespaces_rule = RuleWhitespaces(self._text, self._next_index)
                if whitespaces_rule.matches():
                    self._next_index = whitespaces_rule.get_next_index_to_match()
                    self._update_furthest_matched_index()
                    # Ignoring the tokens because whitespaces here are not meaningful
                
                if not self._text.startswith(KEY_VAL_CONNECTOR, self._next_index):
                    self.error_msg = \
                        "Cannot mix key-value pairs and single values " + \
                        "in annotations. Expected a key-value connector " + \
                        "(using symbol '" + KEY_VAL_CONNECTOR + "')."
                    return False
                self._next_index += 1
                self._update_furthest_matched_index()
                self._tokens.append(
                    LexicalToken(
                        TerminalType.key_value_connector, KEY_VAL_CONNECTOR
                    )
                )

                whitespaces_rule = RuleWhitespaces(self._text, self._next_index)
                if whitespaces_rule.matches():
                    self._next_index = whitespaces_rule.get_next_index_to_match()
                    self._update_furthest_matched_index()
                    # Ignoring the tokens because whitespaces here are not meaningful

                value_rule = RuleKeyValue(self._text, self._next_index)
                if not value_rule.matches(extracting_key=False):
                    self.error_msg = value_rule.error_msg
                    self._update_furthest_matched_index(value_rule)
                    return False
                self._next_index = value_rule.get_next_index_to_match()
                self._update_furthest_matched_index(value_rule)
                self._tokens.extend(value_rule.get_lexical_tokens())

                whitespaces_rule = RuleWhitespaces(self._text, self._next_index)
                if whitespaces_rule.matches():
                    self._next_index = whitespaces_rule.get_next_index_to_match()
                    self._update_furthest_matched_index()
                    # Ignoring the tokens because whitespaces here are not meaningful
        
        if not self._text.startswith(ANNOTATION_END, self._next_index):
            self.error_msg = \
                "Invalid token. Expected the annotation to end there (using " + \
                "character ')')."
            return False
        self._next_index += 1
        self._update_furthest_matched_index()
        self._tokens.append(
            LexicalToken(TerminalType.annotation_end, ANNOTATION_END)
        )
        return True
