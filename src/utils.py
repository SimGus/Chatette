#!/usr/bin/env python3

import sys


def printDBG(txt):
    print("[DBG] "+txt)


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


if __name__ == "__main__":
    import warnings
    warnings.warn("You are running the wrong file ('utils.py')." +
        "The file that should be run is 'main.py'.")
