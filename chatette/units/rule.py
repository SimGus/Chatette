# coding: utf-8

"""
Module `chatette.units.rule`
Contains a class representing rules
(as they will be contained in choices and unit definitions).
"""

from chatette.units.generating_item import GeneratingItem
from chatette.units import Example, sort_by_texts, add_example_no_dup
from chatette.modifiers.randgen import \
    can_concat_examples, concat_examples_with_randgen

from chatette.parsing.utils import SLOT_VAL_SYM


class Rule(GeneratingItem):
    """
    Represents a rule (as it will be contained in choices or unit definitions).
    """
    def __init__(self, parent_name=None, contents=None, slot_value=None):
        self.parent_name = parent_name
        super(Rule, self).__init__(None, leading_space=False)
        self._contents = contents

        self._max_nb_cached_ex = 0

        self.slot_value = slot_value

    def _compute_full_name(self):
        if self.parent_name is not None:
            return "rule contained in " + self.parent_name
        return "rule not contained in anything"

    def get_max_cache_size(self):
        return 0

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
                        if can_concat_examples(ex, content_ex):
                            new_example = \
                                concat_examples_with_randgen(ex, content_ex)
                            add_example_no_dup(tmp_buffer, new_example)
                generated_examples = tmp_buffer
        if generated_examples is None:
            return []
        return sort_by_texts(generated_examples)


    def __str__(self):
        result = self.full_name + ": "
        if len(self._contents) == 0:
            result += "no contents"
        else:
            for content in self._contents:
                result += str(content) + ", "
        return '<' + result + '>'

    def as_template_str(self):
        result = ""
        for content in self._contents:
            result += content.as_template_str()
        if self.slot_value is not None:
            result += ' ' + SLOT_VAL_SYM + ' ' + self.slot_value
        return result
