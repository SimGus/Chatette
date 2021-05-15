#!/usr/bin/env python3
# coding: utf-8
"""
Module `chatette.log`
Contains logging functions used throughout the project.
"""

import sys


# pylint: disable=invalid-name
def print_DBG(txt):
    """Prints debug information on stdout."""
    print("[DBG] " + txt)


def print_warn(txt):
    """Warns the user using stdout."""
    print("\n[WARN] " + txt + "\n", file=sys.stderr)
