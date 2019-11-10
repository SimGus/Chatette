# coding: utf-8
"""
Module `chatette.configuration`
Contains the singleton storing the current configuration
of the program.
"""

from chatette.utils import Singleton, print_warn


class Configuration(Singleton):
    """
    Singleton containing the current configuration of
    the whole program.
    """
    _instance = None
    def __init__(self):
        self.caching_level = 100  # out of 100

    def set_caching_level(self, new_level):
        print_warn(
            "Setting caching level to " + str(new_level) + \
            " for performance reasons."
        )
        if new_level < 0 or new_level > 100:
            raise ValueError(
                "Tried to set the caching level to an invalid level (" + \
                str(new_level) + ")."
            )
        self.caching_level = new_level
