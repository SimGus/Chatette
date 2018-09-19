#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from random import randint


def printDBG(txt):
    print("[DBG] "+txt)
def printWarn(txt):
    print("[WARN] "+txt)


def cast_to_unicode(any):
    if sys.version_info[0] == 3:
        return any
    if isinstance(any, str):
        return unicode(any, "utf-8")
    elif isinstance(any, dict):
        cast_dict = dict()
        for key in any:
            cast_key = cast_to_unicode(key)
            cast_value = cast_to_unicode(any[key])
            cast_dict[cast_key] = cast_value
        return cast_dict
    elif isinstance(any, list):
        cast_list = []
        for e in any:
            cast_list.append(cast_to_unicode(e))
        return cast_list
    else:
        return any


def choose(list):
    """Same as `random.choice(list)` but doesn't throw an error if list is empty"""
    # ([anything]) -> anything or None
    list_len = len(list)
    if list_len <= 0:
        return None
    return list[randint(0, list_len-1)]


if __name__ == "__main__":
    import warnings
    warnings.warn("You are running the wrong file ('utils.py')." +
        "The file that should be run is 'run.py'.")
