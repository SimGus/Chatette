#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.utils`
Contains utility functions used everywhere in the project.
"""

from __future__ import print_function
import sys
from random import randint


# pylint: disable=invalid-name
def print_DBG(txt):
    """Prints debug information on stdout."""
    print("[DBG] " + txt)


def print_warn(txt):
    """Warns the user using stdout."""
    print("[WARN] " + txt)


def cast_to_unicode(anything):
    """
    If executed with Python 2.7, cast any string that is in `anything`
    to unicode.
    If executed with Python 3, returns `anything`.
    `anything` can be a string, an array, a dict,...
    """
    if sys.version_info[0] == 3:
        return anything

    if isinstance(anything, str):
        return unicode(anything, "utf-8")
    if isinstance(anything, dict):
        cast_dict = dict()
        for key in anything:
            cast_key = cast_to_unicode(key)
            cast_value = cast_to_unicode(anything[key])
            cast_dict[cast_key] = cast_value
        return cast_dict
    if isinstance(anything, list):
        cast_list = []
        for e in anything:
            cast_list.append(cast_to_unicode(e))
        return cast_list
    return anything


def choose(array):
    """
    Same as `random.choice(array)` but doesn't throw an error
    if `array` is empty
    """
    # ([anything]) -> anything or None
    array_len = len(array)
    if array_len <= 0:
        return None  # None and not [] (it is used later on in the code)
    return array[randint(0, array_len - 1)]


def rchop(string, ending):
    """Removes a substring at the end of a string."""
    if string.endswith(ending):
        return string[:-len(ending)]
    return string


def str_to_bool(text):
    """
    Transforms the strings 'True' and 'False' to their boolean counterparts.
    Raises a `ValueError` if `text` is neither of them.
    """
    text = text.lower()
    if text == "true":
        return True
    if text == "false":
        return False
    raise ValueError("Cannot convert '" + str(text) + "' into a boolean")


def remove_duplicates(dict_of_lists):
    """Removes duplicates from a dictionary containing lists."""
    return {key: list(set(value)) for (key, value) in dict_of_lists.items()}



if __name__ == "__main__":
    # pylint: disable=wrong-import-position
    import warnings

    warnings.warn("You are running the wrong file ('utils.py')." +
                  "The file that should be run is 'run.py'.")
