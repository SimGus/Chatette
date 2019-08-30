# coding: utf-8
"""
Module `chatette.modifiers.argument`
Contaisn the different functions that allow to apply
the argument generation modifier to one or several examples.
"""

from chatette.parsing.utils import ARG_SYM


def modify_nb_possibilities(unmodified_nb_possibilities):
    """
    Returns the number of possibilities of generation for an item that has
    an argument modifier, given the number of possibilities for
    the same item without this modifier.
    """
    return unmodified_nb_possibilities


def modify_example(example, arg_mapping):
    """
    Modifies the generated example `example` by applying
    the argument modifier with the mapping `arg_mapping` between
    the argument names and values.
    Returns the modified example.
    """
    for arg_name in arg_mapping:
        to_replace = ARG_SYM + arg_name
        example.text = example.text.replace(to_replace, arg_mapping[arg_name])
    return example


def make_all_possibilities(examples, arg_mapping):
    """
    Given the list of examples `examples`, constructs and returns a list
    of all possible examples after the argument modifier applied
    using the mapping `arg_mapping` between the argument names and values.
    """
    for ex in examples:
        modify_example(ex, arg_mapping)
    return examples
