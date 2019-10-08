# coding: utf-8
"""
Module `chatette.modifiers.randgen`
Contains the different functions taht allow to apply
the random generation modifier to one or several examples.
"""

from random import randrange
from copy import deepcopy

from chatette.units import add_example_no_dup


RANDGEN_MAPPING_KEY = "randgen_mapping"


def modify_nb_possibilities(unmodified_nb_possibilities):
    """
    Returns the number of possibilities of generation for an item that has
    a random generation modifier, given the number of possibilities for
    the same item without this modifier.
    """
    return unmodified_nb_possibilities + 1


def should_generate(
    randgen_name, percentgen, opposite=False, randgen_mappings=None
):
    """
    Returns `True` if the current item should generate
    given the name of the current random generation `randgen_name`
    (if there is one), the percentage `percentgen`
    associated to the current item, whether it is an "opposite randgen" and
    the choices of random generation names made previously `randgen_mappings`.
    """
    if randgen_name is None:
        return randrange(100) < percentgen
    if randgen_name not in randgen_mappings:
        randgen_mappings[randgen_name] = (randrange(100) < percentgen)
    if opposite:
        return not randgen_mappings[randgen_name]
    return randgen_mappings[randgen_name]


def make_all_possibilities(
    examples, empty_example, randgen_name=None, opposite=False
):
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
                    "' to already be set (for example with text '" + \
                    str(ex.text) + "')."
                )
            current_randgen_mapping[randgen_name] = not opposite
            setattr(ex, RANDGEN_MAPPING_KEY, current_randgen_mapping)
        
        current_randgen_mapping = \
            getattr(empty_example, RANDGEN_MAPPING_KEY, dict())
        if randgen_name in current_randgen_mapping:
            raise KeyError(
                "Didn't expect the random generation name '" + randgen_name + \
                "' to already be set (for empty example)."
            )
        current_randgen_mapping[randgen_name] = opposite
        setattr(empty_example, RANDGEN_MAPPING_KEY, current_randgen_mapping)

    return add_example_no_dup(examples, empty_example)


def can_concat_examples(example1, example2):
    """
    Returns `True` iff the random generation names that are common to both
    mappings of examples `example1` and `example2` are associated with
    the same boolean value.
    """
    mapping1 = getattr(example1, RANDGEN_MAPPING_KEY, None)
    mapping2 = getattr(example2, RANDGEN_MAPPING_KEY, None)
    if mapping1 is None or mapping2 is None:
        return True

    for randgen_name in mapping1:
        if (
            randgen_name in mapping2
            and mapping1[randgen_name] != mapping2[randgen_name]
        ):
            return False
    return True

def merge_randgen_mappings(example1, example2):
    """
    Returns the random generation mapping that corresponds to the union
    of that of both examples `example1` and `example2`.
    @pre: both mappings can be merged together.
    """
    mapping1 = getattr(example1, RANDGEN_MAPPING_KEY, None)
    mapping2 = getattr(example2, RANDGEN_MAPPING_KEY, None)
    if mapping1 is None:
        return deepcopy(mapping2)
    if mapping2 is None:
        return deepcopy(mapping1)
    
    result = deepcopy(mapping1)
    for randgen_name in mapping2:
        if randgen_name not in result:
            result[randgen_name] = deepcopy(mapping2[randgen_name])
    return result

def concat_examples_with_randgen(example, example_to_append):
    """
    Returns the concatenation of examples `example` and `example_to_append`
    taking into account their randgen mappings.
    @pre: the randgen mappings of those examples can be merged.
    """
    result = deepcopy(example)
    result.append(deepcopy(example_to_append))
    mapping = merge_randgen_mappings(example, example_to_append)
    if mapping is not None:
        setattr(result, RANDGEN_MAPPING_KEY, mapping)
    return result
