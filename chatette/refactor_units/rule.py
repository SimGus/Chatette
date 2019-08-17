# coding: utf-8

"""
Module `chatette.refactor_units.rule`
Contains a class representing rules
(as they will be contained in choices and unit definitions).
"""


from copy import deepcopy

from chatette.refactor_units.generating_item import GeneratingItem
from chatette.refactor_units import Example


class Rule(GeneratingItem):
    """
    Represents a rule (as it will be contained in choices or unit definitions).
    """
    def __init__(self, parent_name=None, contents=None):
        self.parent_name = parent_name
        super(Rule, self).__init__(None, leading_space=False)
        self._contents = contents
    
    def _compute_full_name(self):
        return "rule contained in " + self.parent_name
    
    def _compute_nb_possibilities(self):
        if len(self._contents) == 0:
            return 1
        acc = None
        for content in self._contents:
            if acc is None:
                acc = content.get_max_nb_possibilities()
            else:
                acc *= content.get_max_nb_possibilities()
        return acc
    
    def _generate_random_strategy(self):
        generated_example = Example()
        randgen_mapping = dict()
        for content in self._contents:
            generated_example.append(
                content.generate_random(randgen_mapping=randgen_mapping)
            )
        return generated_example
    
    def _generate_all_strategy(self):
        if len(self._contents) == 0:
            return []
        generated_examples = None
        for content in self._contents:
            tmp_buffer = []
            content_examples = content.generate_all()
            if generated_examples is None:
                generated_examples = content_examples
            else:
                for ex in generated_examples:
                    for content_ex in content_examples:
                        new_example = deepcopy(ex)
                        new_example.append(content_ex)
                        tmp_buffer.append(new_example)
                generated_examples = tmp_buffer
        return generated_examples
