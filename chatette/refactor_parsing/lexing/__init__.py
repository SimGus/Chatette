# -*- coding: utf-8 -*-
"""
Module `chatette.refactor_parsing.lexing`
Contains every class that has to do with lexing
(transforming a text in a sequence of labelled tokens).
"""


class LabelledToken(object):
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
            "LabelledToken(type: " + self.type.name + \
            ", tokens: \"" + self.token + "\")"
