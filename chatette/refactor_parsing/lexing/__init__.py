# -*- coding: utf-8 -*-
"""
Module `chatette.refactor_parsing.lexing`
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
    separator = 19
    encloser = 20
    # Rule contents
    word = 21
    choice_start = 22
    choice_end = 23
    choice_sep = 24
    unit_ref_start = 25
    unit_ref_end = 26
    slot_val_marker = 27  # '='
    slot_val = 28
    # Modifiers
    casegen_marker = 29
    arg_marker = 30
    arg_name = 31
    arg_value = 32
    arg_start = 33  # '('
    arg_end = 34  # ')'
    randgen_marker = 35
    randgen_name = 36
    percentgen_marker = 37
    percentgen = 38
    variation_marker = 39
    variation_name = 40


class LexicalToken(object):
    """Represents a terminal token with a given `TerminalType`."""
    def __init__(self, terminal_type, token_text):
        self.type = terminal_type
        if len(token_text) == 0 and (self.type != TerminalType.ignore):
            raise ValueError("Tried to create a lexed item of 0 characters.")
        self.token = token_text
    
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return \
            "LexicalToken(type: " + self.type.name + \
            ", tokens: \"" + self.token + "\")"
