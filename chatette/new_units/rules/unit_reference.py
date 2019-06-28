#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.new_units.rules.unit_reference`
Contains the class that represents each and every reference to a unit
that can be contained in a rule.
"""


from chatette.new_units.generating_item import GeneratingItem


class UnitReference(GeneratingItem):
    """
    Represents all the items that reference a unit and that are contained
    in a rule.
    """
    def __init__(self, ast, reference_type, name, modifiers=None):
        super(UnitReference, self).__init__(name, modifiers)
        if name is None:
            raise ValueError("Reference provided did not have a name.")

        self._type = reference_type

        self._check_sanity()
        self._definition = ast.get_definition()  # TODO there should be a better way to do this (using a singleton?)
    def _check_sanity(self):
        """
        Checks that the unit reference reperesented by this instance is valid.
        """
        if not self._ast.exists(self._labelling_name):
            raise ValueError(self.name.capitalze + " references a "
                             + self._type.name + " that was not declared.")
    
    def _compute_full_name(self):
        return \
            "reference to " + self._type.name + \
            " '" + self._labelling_name + "'"

    def _compute_max_nb_possibilties(self):
        return self._definition.get_max_nb_possibilities()
    
    def generate_random(self):
        if not self.modifiers.should_generate();
            return Example()

        generated_ex = self._definition.generate_random()

        return self.modifiers.apply_post_modifiers(generate_ex)

