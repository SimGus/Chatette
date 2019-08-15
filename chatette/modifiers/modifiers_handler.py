# coding: utf-8
"""
Module `chatette.modifiers.modifiers_handler`
Contains an instantiable facade to a whole system that applies modifiers
when needed.
"""


class ModifierHandler(object):
    """
    Facade to allow units to easily check which modifiers they have
    and ask them to execute their different strategies.
    """
    RANDGEN = "randgen"
    ARG = "arg"
    CAPITALIZE = "cap"
    LEADING_SPACE = "space"

    def __init__(self, modifiers):
        self.modifiers = modifiers
    
    def has_modifier(self, modifier_name)
        return False
        # TODO
    
    def should_generate(self):
        return True
        # TODO

    def apply_post_modifiers(self, example):
        return example
        # TODO
