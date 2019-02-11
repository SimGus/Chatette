import random
#from typing import List

from chatette.units import UnitDefinition#, Example
from .example import IntentExample


class IntentDefinition(UnitDefinition):
    """
    This class represents the definition of an intent,
    containing all the rules it can generate from.
    """

    def __init__(self, name, modifiers, rules=None):
        super(IntentDefinition, self).__init__(name, modifiers, rules=rules)

        self.type = "intent"
        self.nb_training_examples_asked = None  # All possibilities will be generated TODO
        self.nb_testing_examples_asked = None

    def set_nb_examples_asked(self, nb_training_examples_asked, nb_testing_examples_asked=None):
        self.nb_training_examples_asked = nb_training_examples_asked
        self.nb_testing_examples_asked = nb_testing_examples_asked


    def generate_random(self, variation_name=None, arg_value=None):
        example = \
            super(IntentDefinition, self).generate_random(variation_name, arg_value)
        tmp = IntentExample.from_example(self.name, example)
        return tmp
    
    def generate_all(self, variation_name=None, arg_value=None):
        examples = \
            super(IntentDefinition, self).generate_all(variation_name, arg_value)
        return [IntentExample.from_example(self.name, ex) for ex in examples]

    def generate(self, max_nb_examples, training_examples=None):# -> List[Example]:
        """
        Generates all the examples that were asked (i.e. as much examples
        as asked). The number of generated examples is tied to a maximum though TODO.
        When `training_examples` is `None`, this will generate the training examples
        (i.e. the number of training examples asked); otherwise, it will generate
        examples that are not in `training_examples` (if possible).
        """
        if training_examples is None and self.nb_training_examples_asked is None:
            return [
                    IntentExample(self.name, ex.text.strip(), ex.entities)
                    for (i, ex) in enumerate(self.generate_all())
                    if i < max_nb_examples
                ]

        nb_examples_asked = self.nb_training_examples_asked
        if training_examples is not None:
            if self.nb_testing_examples_asked is None:
                return []  # No examples must be generated
            nb_examples_asked = self.nb_testing_examples_asked

        if nb_examples_asked <= 0:
            return []

        nb_possible_ex = self.get_max_nb_generated_examples()
        if nb_examples_asked > nb_possible_ex:
            if training_examples is None:
                return [
                    IntentExample(self.name, ex.text.strip(), ex.entities)
                    for (i, ex) in enumerate(self.generate_all())
                    if i < max_nb_examples
                ]

            all_examples = [
                IntentExample(self.name, ex.text.strip(), ex.entities)
                for (i, ex) in enumerate(self.generate_all())
                if i < max_nb_examples
            ]
            return [
                ex
                for ex in all_examples if ex not in training_examples
            ]

        if nb_examples_asked > max_nb_examples:
            nb_examples_asked = max_nb_examples

        if nb_examples_asked < nb_possible_ex / 2:  # QUESTION: should this be /2?
            generated_examples = []
            for _ in range(nb_examples_asked):
                nb_iterations = 0
                while nb_iterations < 50:  # 50 is completely arbitrary
                    current_example = self.generate_random()
                    current_example.text = current_example.text.strip()  # Strip for safety
                    if (    current_example not in generated_examples
                        and (training_examples is None
                             or current_example not in training_examples)):
                        generated_examples.append(
                            IntentExample(self.name, current_example.text,
                                          current_example.entities))
                        break
                    nb_iterations += 1
            return generated_examples

        all_examples = [
            IntentExample(self.name, ex.text.strip(), ex.entities)
            for ex in self.generate_all()
        ]

        if training_examples is None:
            return random.sample(all_examples, nb_examples_asked)
        random.shuffle(all_examples)
        return [
            ex for ex in all_examples
            if ex not in training_examples
        ]


    def _get_template_decl(self, variation=None):
        result = '%' + \
                 super(IntentDefinition, self)._get_template_decl(variation)
        if self.nb_training_examples_asked is not None:
            result += "(train:" + str(self.nb_training_examples_asked)
            if self.nb_testing_examples_asked is not None:
                result += ", test:" + str(self.nb_testing_examples_asked) + ')'
        elif self.nb_testing_examples_asked is not None:
            result += "(test:" + str(self.nb_testing_examples_asked) +')'
        return result

    def short_desc_str(self):
        """
        Returns a str representing a short description of this unit description.
        """
        desc = super(IntentDefinition, self).short_desc_str() + '\n'
        if self.nb_training_examples_asked is None:
            desc += "# training examples: all\n"
        else:    
            desc += "# training examples: " + \
                    str(self.nb_training_examples_asked) + '\n'
        if self.nb_testing_examples_asked is None:
            desc += "# testing examples: all"
        else:
            desc += "# testing examples: " + str(self.nb_testing_examples_asked)
        return desc
