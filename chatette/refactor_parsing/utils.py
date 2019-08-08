# -*- coding: utf-8 -*-
"""
Module `chatette.refactor_parsing.utils`
Contains utility functions that are used by various parsing components.
"""

from enum import Enum
from chatette.utils import min_if_exist


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
CHOICE_START = '['
CHOICE_END = ']'
CHOICE_SEP = '|'
OLD_CHOICE_START = '{'
OLD_CHOICE_END = '}'
OLD_CHOICE_SEP = '/'
# Modifiers
CASE_GEN_SYM = '&'
RAND_GEN_SYM = '?'
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
        return current_index-len(str_to_find)
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

def extract_annotation_key_value(text, start_index):
    """
    Extracts the key/value that starts at `start_index` in `text`.
    Returns the key/value, or an empty text if none was found.
    If `start_index` points to the end of the text, returns `None`.
    If there is just one encloser, returns it with the key/value.
    """
    if start_index == len(text):
        return None
    if text[start_index] in KEY_VAL_ENCLOSERS:
        encloser = text[start_index]
        end_index = find_unescaped(text, encloser, start_index+1)
        if end_index is not None:
            return text[start_index+1:end_index]
        else:
            return text[start_index:]
    else:
        end_annotation = find_unescaped(text, ANNOTATION_END, start_index)
        if end_annotation is not None:
            return text[start_index:end_annotation]
        else:
            return text[start_index:]
        

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


def remove_enclosers(text):
    """
    Returns the contents of `text` where the enclosers have been removed.
    If no enclosers were found, returns `text`.
    Returns `None` if there is just one encloser or the enclosers don't match
    each other.
    """
    if len(text) == 0:
        return text
    if text[0] in KEY_VAL_ENCLOSERS:
        encloser = text[0]
        if text.endswith(encloser):
            return text[1:-1]
        return None
    return text
