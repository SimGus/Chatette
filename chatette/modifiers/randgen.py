# coding: utf-8
"""
Module `chatette.modifiers.randgen`
Contains the different functions taht allow to apply
the random generation modifier to one or several examples.
"""

from random import randrange

from chatette.refactor_units import Example


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
    print("should generate?")
    if randgen_name is None:
        print("no randgen name")
        return randrange(100) < percentgen
    if randgen_name not in randgen_mappings:
        print("randgen name not in mapping")
        randgen_mappings[randgen_name] = (randrange(100) < percentgen)
    print("done")
    return randgen_mappings[randgen_name]


def make_all_possibilities(examples):
    """
    Given the list of examples `examples`, constructs and returns a list
    of all possible examples after the random generation modifier applied.
    """
    examples.append(Example())  # TODO keep the randgen mapping in the example? Id. for the other ones?
    return examples
