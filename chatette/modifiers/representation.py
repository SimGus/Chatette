# coding: utf-8
"""
Module `chatette.modifiers.representation`
Contains structures that represent the possible modifiers
that could apply to unit declarations or sub-rules.
"""


class ModifiersRepresentation(object):
    def __init__(self):
        self.casegen = False

        self.variation_name = None  # Only for unit references

        self.randgen = False
        self.randgen_name = None
        self.randgen_percent = 50

        self.argument_name = None
        self.argument_value = None  # Should be an OrderedDict {name -> value} sorted in decreasing length of keys (but should be just the arg value as a str at first for single argument)

    def __repr__(self):
        return \
            self.__class__.__name__ + "(casegen: " + str(self.casegen) + \
            " randgen: " + str(self.randgen_name) + " (" + \
            str(self.randgen_percent) + \
            ") arg name: " + str(self.argument_name) + " arg value: " + \
            str(self.argument_value) + ")"
    def __str__(self):
        return self.__repr__()
    
    def short_description(self):
        """
        Returns a short description (as a `str`) that can be displayed to the
        user.
        """
        at_least_one_modifier = False
        desc = ""
        if self.casegen:
            desc += "- case generation\n"
            at_least_one_modifier = True
        if self.randgen:
            desc += "- random generation"
            if self.randgen_name is not None:
                desc += ": " + self.randgen_name
            desc += " (" + str(self.randgen_percent) + "%)\n"
            at_least_one_modifier = True
        if self.argument_name is not None:
            desc += "- argument name: " + self.argument_name + "\n"
            at_least_one_modifier = True
        if self.argument_value is not None:
            desc += "- argument value: " + self.argument_value + "\n"
            at_least_one_modifier = True

        if not at_least_one_modifier:
            desc = "No modifiers\n"
        else:
            desc = "Modifiers:\n" + desc
        return desc
