# coding: utf-8
"""
Module `chatette.parsing.lexing.rule_key_value`
Contains the definition of the class that represents the lexing rule
to tokenize a key or a value inside an annotation.
"""

from chatette.parsing.lexing.lexing_rule import LexingRule
from chatette.parsing.lexing import LexicalToken, TerminalType
from chatette.parsing.utils import \
    ANNOTATION_END, ANNOTATION_SEP, KEY_VAL_CONNECTOR, \
    KEY_VAL_ENCLOSERS, \
    find_unescaped
from chatette.utils import min_if_exist


class RuleKeyValue(LexingRule):
    def _apply_strategy(self, **kwargs):
        """
        `kwargs` can contain a value with key `extracting_key`.
        `extracting_key` is a boolean that is `True` if this rule should extract 
        a key and `False` if this rule should extract a value.
        If `kwargs` doesn't contain `extracting_key`, defaults to `True`.
        """
        extracting_key = kwargs.get("extracting_key", True)
        if extracting_key:
            terminal_type = TerminalType.key
        else:
            terminal_type = TerminalType.value

        encloser = None
        for current_encloser in KEY_VAL_ENCLOSERS:
            if self._text.startswith(current_encloser, self._next_index):
                self._next_index += 1
                self._update_furthest_matched_index()
                encloser = current_encloser
                break
        
        if encloser is not None:
            # Enclosed key/value
            next_encloser_index = \
                find_unescaped(self._text, encloser, self._next_index)
            if next_encloser_index is None:
                self.error_msg = \
                    "Missing key-value encloser. Expected symbol " + encloser + \
                    " instead of end of line."
                return False

            extracted_text = self._text[self._start_index+1:next_encloser_index]
            self._next_index = next_encloser_index + 1
            self._update_furthest_matched_index()
            self._tokens.append(LexicalToken(terminal_type, extracted_text))
            return True
        else:
            # Key/value not enclosed
            end_annotation_index = \
                find_unescaped(self._text, ANNOTATION_END, self._next_index)
            if extracting_key:
                next_connector_index = \
                    find_unescaped(
                        self._text, KEY_VAL_CONNECTOR, self._next_index
                    )
                end_key_value_index = \
                    min_if_exist(next_connector_index, end_annotation_index)
            else:  # Extracting value
                next_key_val_pair_index = \
                    find_unescaped(
                        self._text, ANNOTATION_SEP, self._next_index
                    )
                end_key_value_index = \
                    min_if_exist(next_key_val_pair_index, end_annotation_index)

            if end_key_value_index is None:
                self.error_msg = \
                    "Couldn't find the end of key/value. " + \
                    "Didn't expect the end of the line there."
                return False
            
            extracted_text = \
                self._text[self._start_index:end_key_value_index].rstrip()
            self._next_index += len(extracted_text)
            self._update_furthest_matched_index()
            self._tokens.append(LexicalToken(terminal_type, extracted_text))

            return True
