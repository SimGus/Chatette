# coding: utf-8
"""
Module `chatette.parsing.utils`
Contains utility functions that are used by various parsing components.
"""

from enum import Enum

from chatette.utils import min_if_exist, UnitType
from chatette.parsing.lexing import TerminalType


######## Symbols definitions ########
ESCAPEMENT_SYM = '\\'
# Comments
COMMENT_SYM = '//'
OLD_COMMENT_SYM = ';'
# File inclusion
FILE_INCLUSION_SYM = '|'
# Unit declarations/references
UNIT_START_SYM = '['
UNIT_END_SYM = ']'
ALIAS_SYM = '~'
SLOT_SYM = '@'
INTENT_SYM = '%'
# Annotations
ANNOTATION_START = '('
ANNOTATION_END = ')'
ANNOTATION_SEP = ','
KEY_VAL_CONNECTOR = ':'
KEY_VAL_ENCLOSERS = ["'", '"']
# Unit rules
SLOT_VAL_SYM = '='
SLOT_VAL_FIRST_RULE = '/'
CHOICE_START = '['
CHOICE_END = ']'
CHOICE_SEP = '|'
OLD_CHOICE_START = '{'
OLD_CHOICE_END = '}'
OLD_CHOICE_SEP = '/'
# Modifiers
CASE_GEN_SYM = '&'
RAND_GEN_SYM = '?'
RAND_GEN_PERCENT_SYM = '/'
ARG_SYM = '$'
VARIATION_SYM = '#'


def find_unescaped(text, str_to_find, start_index=0, end_index=None):
    """
    Finds the first occurrence of `str_to_find` in `text`
    and returns its first index.
    Returns `None` if nothing was found.
    The search is restricted to characters between `start_index` and
    `end_index` (if provided).
    `start_index` is included and `end_index` excluded.
    @pre: `str_to_find` should not contain escapements.
    """
    length = len(text)
    if len(str_to_find) == 0 or len(str_to_find) > length:
        return None
    if end_index is None:
        end_index = length
    
    current_index = start_index
    to_find_index = 0
    escaped = False
    while current_index < end_index:
        if escaped:
            escaped = False
        elif text[current_index] == ESCAPEMENT_SYM:
            escaped = True
        else:
            escaped = False
            if text[current_index] == str_to_find[to_find_index]:
                to_find_index += 1
            else:
                to_find_index = 0

        current_index += 1
        if to_find_index == len(str_to_find):
            break
    
    if to_find_index == len(str_to_find):
        return current_index - len(str_to_find)
    return None


def find_next_comment(text, start_index=0, end_index=None):
    """
    Finds the next comment in `text` starting from `start_index`
    until `end_index` (or the end of the text if it wasn't provided).
    Detects both new-style comments ('//') and old-style comments (';').
    @returns: the index of the beginning of the comment, or `None` if
              if no comment was found.
    """
    if end_index is None:
        end_index = len(text)
        
    comment_index = find_unescaped(text, COMMENT_SYM, start_index, end_index)
    old_comment_index = find_unescaped(
        text, OLD_COMMENT_SYM, start_index, end_index
    )
    return min_if_exist(comment_index, old_comment_index)


def extract_identifier(text, start_index=0):
    """
    Returns the part of `text` that starts at `start_index` and
    correponds to an identifier, key, value, argument name, randgen name,...
    Returns an empty string if no identifier was found.
    Returns `None` if `start_index` points to the end of the string.
    @raises: `ValueError` if `start_index` points to further than the end of
             `text`.
    """
    length = len(text)
    if start_index == length:
        return None
    elif start_index > length:
        raise ValueError("Tried to extract an identifier from outside a string.")
    
    i = start_index
    escaped = False
    while i < length:
        if escaped:
            escaped = False
            i += 1
            continue
        if text[i] == ESCAPEMENT_SYM:
            escaped = True
        elif (
            is_special_identifier_char(text[i]) \
            or text.startswith(COMMENT_SYM, i)
        ):
            break
        i += 1
    if i == start_index:
        return ""
    return text[start_index:i].rstrip()
        

def is_special_identifier_char(c):
    """
    Returns `True` iff character `c` should be escaped in an identifier
    (i.e. it is a special character).
    """
    return c in (
        ESCAPEMENT_SYM, OLD_COMMENT_SYM, FILE_INCLUSION_SYM, UNIT_START_SYM,
        UNIT_END_SYM, ALIAS_SYM, SLOT_SYM, INTENT_SYM,
        CHOICE_START, CHOICE_END, CHOICE_SEP, OLD_CHOICE_START, OLD_CHOICE_END,
        OLD_CHOICE_SEP, CASE_GEN_SYM, RAND_GEN_SYM, ARG_SYM, VARIATION_SYM
    )


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

def index_end_choice_rules(tokens, start_index):
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
    if i > 0 and tokens[i].type == TerminalType.randgen_marker:
        i -= 1
    return i


def get_template_unit_sym(unit_type):
    """Returns the symbol that corresponds to unit type `unit_type`."""
    if unit_type == UnitType.alias:
        return ALIAS_SYM
    if unit_type == UnitType.slot:
        return SLOT_SYM
    if unit_type == UnitType.intent:
        return INTENT_SYM
    raise TypeError(
        "Tried to get the symbol associated to an invalid unit type: '" + \
        unit_type.__class__.__name__ + "'."
    )
def get_template_pre_modifiers(modifiers_repr):
    """
    Returns the string of pre-modifiers as a string that would be found in
    a template file.
    """
    if modifiers_repr.casegen:
        return CASE_GEN_SYM
    return ""
def get_template_post_modifiers(modifiers_repr):
    """
    Returns the string of pre-modifiers as a string that would be found in
    a template file.
    """
    result = ""
    if modifiers_repr.randgen:
        result += RAND_GEN_SYM
        if modifiers_repr.randgen_name is not None:
            result += modifiers_repr.randgen_name
        if modifiers_repr.randgen_percent != 50:
            result += \
                RAND_GEN_PERCENT_SYM + str(modifiers_repr.randgen_percent) + '%'
    if modifiers_repr.variation_name is not None:
        result += VARIATION_SYM + modifiers_repr.variation_name
    if modifiers_repr.argument_name is not None:
        result += ARG_SYM + modifiers_repr.argument_name
    elif modifiers_repr.argument_value is not None:
        result += ARG_SYM
        if len(modifiers_repr.argument_value) == 1:
            for (name, value) in modifiers_repr.argument_value.items():
                result += value
        else:
            result += "ERROR"  # TODO do this when the new arg assignment lexing rule has been coded
    return result
