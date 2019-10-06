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

        self.randgen = RandgenRepresentation()

        self.argument_name = None
        self.argument_value = None  # Should be an OrderedDict {name -> value} sorted in decreasing length of keys (but should be just the arg value as a str at first for single argument)

    def __repr__(self):
        return \
            self.__class__.__name__ + "(casegen: " + str(self.casegen) + \
            " randgen: " + str(self.randgen) + \
            " arg name: " + str(self.argument_name) + " arg value: " + \
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
            if self.randgen.name is not None:
                desc += ": " + self.randgen.name
            if self.randgen.opposite:
                desc += " [opposite]"
            desc += " (" + str(self.randgen.percentage) + "%)\n"
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


class RandgenRepresentation(object):
    def __init__(self):
        self._present = False
        self.name = None
        self.opposite = False
        self.percentage = 50

    def __bool__(self):  # For Python 3.x
        return self._present
    def __nonzero__(self):  # For Python 2.7
        return self.__bool__()
    
    def __repr__(self):
        if not self._present:
            return "No"
        result = "Yes"
        if self.name is not None:
            result += " '" + str(self.name) + "'"
        result += " ("
        if self.opposite:
            result += "opposite, "
        result += str(self.percentage) + "%)"
        return result
    def __str__(self):
        return self.__repr__()
