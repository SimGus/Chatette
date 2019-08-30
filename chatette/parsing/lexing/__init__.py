# coding: utf-8
"""
Module `chatette.parsing.lexing`
Contains every class that has to do with lexing
(transforming a text in a sequence of labelled tokens).
"""

from enum import Enum


# Supported tokens
class TerminalType(Enum):
    """Enum of terminals types that will be used by the lexer."""
    # Special
    ignore = 0
    indentation = 1
    whitespace = 2
    comment = 3
    # File inclusion
    file_inclusion_marker = 4
    file_path = 5
    # Unit declaration
    alias_decl_start = 6
    alias_decl_end = 7
    slot_decl_start = 8
    slot_decl_end = 9
    intent_decl_start = 10
    intent_decl_end = 11
    unit_identifier = 12
    # Annotations
    annotation_start = 13
    annotation_end = 14
    separator = 15
    key = 16
    value = 17
    key_value_connector = 18
    encloser = 19
    # Rule contents
    word = 20
    choice_start = 21
    choice_end = 22
    choice_sep = 23
    alias_ref_start = 24
    alias_ref_end = 25
    slot_ref_start = 26
    slot_ref_end = 27
    intent_ref_start = 28
    intent_ref_end = 29
    slot_val_marker = 30  # '='
    slot_val = 31
    # Modifiers
    casegen_marker = 32
    arg_marker = 33
    arg_name = 34
    arg_value = 35
    arg_start = 36  # '('
    arg_end = 37  # ')'
    randgen_marker = 38
    randgen_name = 39
    percentgen_marker = 40
    percentgen = 41
    variation_marker = 42
    variation_name = 43


class LexicalToken(object):
    """Represents a terminal token with a given `TerminalType`."""
    def __init__(self, terminal_type, token_text):
        self.type = terminal_type
        if len(token_text) == 0 and (self.type != TerminalType.ignore):
            raise ValueError("Tried to create a lexed item of 0 characters.")
        self.text = token_text
    
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return \
            "LexicalToken(type: " + self.type.name + \
            ", tokens: \"" + self.text + "\")"
