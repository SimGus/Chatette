#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from warnings import warn

from chatette.utils import print_warn


# ============ Deprecation of semi-colon syntax for comments ===============
# Comments starting with semi-colons ';' are now deprecated to have a closer
# syntax to *Chatito* v2.1.x
_SEMICOLON_COMMENTS_DEPRECATION_WARNED = False


def warn_semicolon_comments():
    """
    Warns the user on stdout that one of their files contains semicolons
    comments (which are a deprecated way of making comments).
    Rather use '//' comments instead of ';' comments.
    """
    global _SEMICOLON_COMMENTS_DEPRECATION_WARNED
    if not _SEMICOLON_COMMENTS_DEPRECATION_WARNED:
        # pylint: disable=bad-continuation
        print_warn("Comments starting with a semi-colon ';' are "+
                   "now deprecated. Rather use the new double slash '//'"+
                   " syntax. This syntax allows to have a syntax closer to "+
                   "Chatito v2.1.x.")
        warn("Comments starting with a semi-colon ';' are now deprecated. " +
             "Rather use the new double slash '//' syntax. This " +
             "syntax allows to have a syntax closer to Chatito v2.1.x.",
             DeprecationWarning)
        _SEMICOLON_COMMENTS_DEPRECATION_WARNED = True
