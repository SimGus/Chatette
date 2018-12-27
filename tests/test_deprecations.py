"""
Test module.
Tests the functions in module 'chatette.utils'.
"""

import chatette.deprecations
from chatette.deprecations import warn_semicolon_comments


def test_several_calls():
    assert not chatette.deprecations._SEMICOLON_COMMENTS_DEPRECATION_WARNED
    warn_semicolon_comments()
    assert chatette.deprecations._SEMICOLON_COMMENTS_DEPRECATION_WARNED
