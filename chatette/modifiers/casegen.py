# coding: utf-8
"""
Module `chatette.modifiers.casegen`
Contains the different functions that allow to apply
the case generation modifier to one or several examples.
"""

from random import random
from copy import deepcopy


def modify_nb_possibilities(unmodified_nb_possibilities):
    """
    Returns the number of possibilities of generation for an item that has
    a case generation modifier, given the number of possibilities for
    the same item without this modifier.
    """
    return 2 * unmodified_nb_possibilities


def modify_example(example):
    """
    Modifies the generated example `example` by applying
    the case generation modifier.
    Returns the modified example.
    """
    if random() < 0.5:
        return with_leading_upper(example)
    return with_leading_lower(example)


def make_all_possibilities(examples):
    """
    Given the list of examples `examples`, constructs and returns a list
    of all possible examples after the case generation modifier applied.
    """
    result = []
    for ex in examples:
        lowercase_ex = with_leading_lower(ex)
        result.append(lowercase_ex)
        uppercase_ex = with_leading_upper(deepcopy(ex))
        if not uppercase_ex.is_dup(lowercase_ex):
            result.append(uppercase_ex)
    return result

############# Utility functions ##############
def may_change_leading_case(text):
    """
    Checks whether the string `text` can
    change the letter case of its leading letter.
    """
    for c in text:
        if c.isalpha():
            return True
        if c.isspace():
            continue
        return False
    return False


def with_leading_upper(example):
    """
    Changes the leading letter of the text of example `example` to uppercase.
    """
    text = example.text
    for (i, c) in enumerate(text):
        if not c.isspace():
            text = text[:i] + text[i].upper() + text[(i + 1):]
            break
    example.text = text
    return example

def with_leading_lower(example):
    """
    Changes the leading letter of the text of example `example` to uppercase.
    """
    text = example.text
    for (i, c) in enumerate(text):
        if not c.isspace():
            text = text[:i] + text[i].lower() + text[(i + 1):]
            break
    example.text = text
    return example
