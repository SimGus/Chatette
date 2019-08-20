# coding: utf-8
"""
Module `chatette.modifiers.randgen`
Contains the different functions taht allow to apply
the random generation modifier to one or several examples.
"""

from random import randrange

from chatette.refactor_units import add_example_no_dup


RANDGEN_MAPPING_KEY = "randgen_mapping"


def modify_nb_possibilities(unmodified_nb_possibilities):
    """
    Returns the number of possibilities of generation for an item that has
    a random generation modifier, given the number of possibilities for
    the same item without this modifier.
    """
    return unmodified_nb_possibilities + 1


def should_generate(randgen_name, percentgen, randgen_mappings=None):
    """
    Returns `True` if the current item should generate
    given the name of the current random generation `randgen_name`
    (if there is one), the percentage `percentgen`
    associated to the current item and the choices of random generation names
    made previously `randgen_mappings`.
    """
    if randgen_name is None:
        return randrange(100) < percentgen
    if randgen_name not in randgen_mappings:
        randgen_mappings[randgen_name] = (randrange(100) < percentgen)
    return randgen_mappings[randgen_name]


def make_all_possibilities(examples, empty_example, randgen_name=None):
    """
    Given the list of examples `examples`, constructs and returns a list
    of all possible examples after the random generation modifier applied.
    Updates the random generation mapping for each example, considering
    that each example in `examples` was generated with a mapping such that
    `randgen_name` was associated to `True`.
    `empty_example` is a new example that has an empty text and no entities.
    @raises: - `KeyError` if `randgen_name` is already present in a random
               generation mapping.
    """
    if randgen_name is not None:
        for ex in examples:
            current_randgen_mapping = getattr(ex, RANDGEN_MAPPING_KEY, dict())
            if randgen_name in current_randgen_mapping:
                raise KeyError(
                    "Didn't expect the random generation name '" + randgen_name + \
                    "' to already be set."
                )
            current_randgen_mapping[randgen_name] = True
            setattr(ex, RANDGEN_MAPPING_KEY, current_randgen_mapping)
        
        current_randgen_mapping = \
            getattr(empty_example, RANDGEN_MAPPING_KEY, dict())
        if randgen_name in current_randgen_mapping:
            raise KeyError(
                "Didn't expect the random generation name '" + randgen_name + \
                "' to already be set."
            )
        setattr(empty_example, RANDGEN_MAPPING_KEY, current_randgen_mapping)

    return add_example_no_dup(examples, empty_example)
