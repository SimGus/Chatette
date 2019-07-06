"""
Module `chatette.refactor_parsing`
Contains the lexer used by the parser and the definition of the tokens it uses.
"""

from enum import Enum

# Supported tokens
class Terminals(enum):
    """Enum of terminals types that will be used by the lexer."""
