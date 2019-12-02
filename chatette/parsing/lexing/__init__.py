# coding: utf-8
"""
Module `chatette.parsing.lexing`
Contains every class that has to do with lexing
(transforming a text in a sequence of labelled tokens).
"""

from enum import Enum
from chatette.parsing.utils import ESCAPEMENT_SYM, ESCAPABLE_CHARS


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
    opposite_randgen_marker = 40
    percentgen_marker = 41
    percentgen = 42
    variation_marker = 43
    variation_name = 44


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
    
    def remove_escapement(self):
        """Removes all the escapement from the text of this token."""
        processed_text = ""
        for i in range(len(self.text) - 1):
            if not (
                self.text[i] == ESCAPEMENT_SYM
                and self.text[i+1] in ESCAPABLE_CHARS
            ):
                processed_text += self.text[i]
        processed_text += self.text[-1]
        self.text = processed_text


def remove_comment_tokens(tokens):
    """
    Returns all the tokens except the ones that correspond to comments (and
    the preceding whitespaces if any).
    """
    if len(tokens) == 0:
        return tokens
    
    comment_index = None
    for (i, token) in enumerate(tokens):
        if token.type == TerminalType.comment:
            comment_index = i
            break
    
    if comment_index is None:
        return tokens
    if comment_index == 0:
        return []
    if tokens[comment_index - 1].type == TerminalType.whitespace:
        return tokens[:comment_index - 1]
    return tokens[:comment_index]


# TODO: unused function?
def extract_annotation_tokens(tokens):
    """
    Given the list of tokens `tokens`,
    returns a list of tokens that correspond to an annotation.
    Returns `None` if there was no annotation in `tokens`.
    """
    if len(tokens) < 2:
        return None

    start_index = None
    end_index = None
    for (i, token) in enumerate(tokens):
        if token.type == TerminalType.annotation_start:
            start_index = i
        if token.type == TerminalType.annotation_end:
            end_index = i
            break

    if start_index is None:
        return None    
    if end_index is None:
        return tokens[start_index:]
    return tokens[start_index:end_index + 1]


def find_matching_choice_end(tokens, start_index):
    """
    Returns the index of the choice end that matches the choice start at
    index `start_index`.
    Returns `None` if there is no matching choice end.
    @raises: - `ValueError` if there is no choice starting at `start_index`.
             - `ValueError` if arguments are inconsistent.
    """
    if tokens[start_index].type != TerminalType.choice_start:
        raise ValueError(
            "Tried to get the matching choice end of something else than a " + \
            "choice start."
        )

    nb_starts_to_match = 0
    i = start_index + 1
    while i < len(tokens):
        token = tokens[i]
        if token.type == TerminalType.choice_start:
            nb_starts_to_match += 1
        elif token.type == TerminalType.choice_end:
            if nb_starts_to_match > 0:
                nb_starts_to_match -= 1
            else:
                return i
        i += 1
    return None

def find_index_last_choice_content(tokens, start_index):
    """
    Returns the index of the last token that makes up the internal rules
    of the choice starting at index `start_index`. In other words,
    the returned index points to the last token before the end of the choice
    or its random generation markers.
    Returns `None` if the choice is incorrectly closed.
    @raises: - `ValueError` if there isno choice starting at `start_index`.
    """
    end_choice_index = find_matching_choice_end(tokens, start_index)
    i = end_choice_index - 1
    if i > 0 and tokens[i].type == TerminalType.percentgen:
        i -= 1
    if i > 0 and tokens[i].type == TerminalType.percentgen_marker:
        i -= 1
    if i > 0 and tokens[i].type == TerminalType.randgen_name:
        i -= 1
    if i > 0 and tokens[i].type == TerminalType.opposite_randgen_marker:
        i -= 1
    if i > 0 and tokens[i].type == TerminalType.randgen_marker:
        i -= 1
    return i
