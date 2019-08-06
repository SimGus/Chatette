# -*- coding: utf-8 -*-
"""
Module `chatette.refactor_parsing.utils`
Contains utility functions that are used by various parsing components.
"""

# Symbols definitions
ESCAPEMENT_SYM = '\\'

COMMENT_SYM = '//'
OLD_COMMENT_SYM = ';'


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
