#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from chatette.utils import printWarn

#============ Deprecation of semi-colon syntax for comments ===============
# Comments starting with semi-colons ';' are now deprecated to have a closer
# syntax to *Chatito* v2.1.x
_SEMICOLON_COMMENTS_DEPRECATION_WARNED = False

def warn_deprecation_semicolon_comments():
    global _SEMICOLON_COMMENTS_DEPRECATION_WARNED
    if not _SEMICOLON_COMMENTS_DEPRECATION_WARNED:
        printWarn("Deprecation warning: Comments starting with a semi-colon "+
                  "';' are now deprecated. "+
                  "Rather use the new double slash '//' syntax. This "+
                  "syntax allows to have a syntax closer to Chatito v2.1.x.")
        _SEMICOLON_COMMENTS_DEPRECATION_WARNED = True
