#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from .units import *
try:
   from chatette.parser_utils import Unit
except ImportError:
   from parser_utils import Unit


class IntentDefinition(UnitDefinition):
    """
    This class represents the definition of an intent,
    containing all the rules it can generate from.
    """
    def __init__(self, name, rules=[], arg=None, casegen=False):
        super(IntentDefinition, self).__init__(name, rules=rules, arg=arg,
            casegen=casegen)
        self.type = "intent"
        self.nb_training_examples_asked = None  # All possibilities will be generated TODO
        self.nb_testing_examples_asked = None

    def set_nb_examples_asked(self, nb_training_examples_asked,
                                    nb_testing_examples_asked=None):
        # int -> ()
        self.nb_training_examples_asked = nb_training_examples_asked
        self.nb_testing_examples_asked = nb_testing_examples_asked


    def generate(self, max_nb_examples, training_examples=None):
        """
        Generates all the examples that were asked (i.e. as much examples
        as asked). The number of generated examples is tied to a maximum though TODO.
        When `training_examples` is `None`, this will generate the training examples
        (i.e. the number of training examples asked), otherwise, it will generate
        examples that are not in `training_examples` (if possible).
        """
        if (    training_examples is None
            and self.nb_training_examples_asked is None):
            return [{"text": ex["text"].strip(), "entities": ex["entities"]}
                    for (i, ex) in enumerate(self.generate_all())
                    if i < max_nb_examples]

        nb_examples_asked = self.nb_training_examples_asked
        if training_examples is not None:
            if self.nb_testing_examples_asked is None:
                return []  # No examples must be generated
            nb_examples_asked = self.nb_testing_examples_asked
        if nb_examples_asked <= 0:
            return []

        nb_possible_ex = self.get_nb_possible_generated_examples()
        if nb_examples_asked > nb_possible_ex:
            if training_examples is None:
                return [{"text": ex["text"].strip(), "entities": ex["entities"]}
                        for (i, ex) in enumerate(self.generate_all())
                        if i < max_nb_examples]
            else:
                all_examples = [{"text": ex["text"].strip(),
                                 "entities": ex["entities"]}
                                for (i, ex) in enumerate(self.generate_all())
                                if i < max_nb_examples]
                return [ex for ex in all_examples
                        if ex not in training_examples]
        if nb_examples_asked > max_nb_examples:
            nb_examples_asked = max_nb_examples

        if nb_examples_asked < nb_possible_ex/2:  # QUESTION: should this be /2?
            generated_examples = []
            for _ in range(nb_examples_asked):
                while True:
                    current_example = self.generate_random()
                    current_example["text"] = current_example["text"].strip()  # Strip for safety
                    if (    current_example not in generated_examples
                        and (   training_examples is None
                             or current_example not in training_examples)):
                        generated_examples.append(current_example)
                        break
            return generated_examples
        else:
            all_examples = [{"text": ex["text"].strip(),
                             "entities": ex["entities"]}
                            for ex in self.generate_all()]
            if training_examples is None:
                return random.sample(all_examples, nb_examples_asked)
            else:
                random.shuffle(all_examples)
                return [ex for ex in all_examples
                        if ex not in training_examples]

    # Everything else is in the superclass


class IntentRuleContent(RuleContent):
    """
    This class represents an intent as it can be contained in a rule,
    with its modifiers.
    Accepted modifiers:
        - leading-space: bool
        - casegen: bool
        - randgen: str
        - percentgen: int
        - arg: str
        - variation-name: str
    """
    def __init__(self, name, leading_space=False, variation_name=None, arg_value=None,
        casegen=False, randgen=None, percentage_gen=50, parser=None):
            super(IntentRuleContent, self).__init__(name, leading_space=leading_space,
                variation_name=variation_name, arg_value=arg_value, casegen=casegen,
                randgen=randgen, percentage_gen=percentage_gen, parser=parser)
            self.casegen_checked = False

    def can_have_casegen(self):
        return self.parser.get_definition(self.name, Unit.intent) \
                          .can_have_casegen()
    def check_casegen(self):
        """Checks that casegen is applicable (at generation time)."""
        if not self.casegen_checked and self.casegen:
            if not self.can_have_casegen():
                self.casegen = False
            self.casegen_checked = True


    def generate_random(self, generated_randgens=dict()):
        self.check_casegen()

        # Manage randgen
        if self.randgen is not None and self.randgen in generated_randgens:
            if generated_randgens[self.randgen]:
                pass  # Must be generated
            else:
                return EMPTY_GEN()  # Cannot be generated
        elif self.randgen is not None:
            if randint(0,99) >= self.percentgen:
                # Don't generated this randgen
                if self.randgen != "":
                    generated_randgens[self.randgen] = False
                return EMPTY_GEN()
            elif self.randgen != "":
                # Generate this randgen
                generated_randgens[self.randgen] = True

        generated_example = self.parser.get_definition(self.name, Unit.intent) \
                                       .generate_random(self.variation_name, \
                                                        self.arg_value)

        if self.casegen:
            generated_example["text"] = \
                randomly_change_case(generated_example["text"])
        if self.leading_space and may_get_leading_space(generated_example["text"]):
            generated_example["text"] = ' '+generated_example["text"]
        return generated_example

    def generate_all(self):
        self.check_casegen()

        generated_examples = []
        if self.randgen is not None:
            generated_examples.append(EMPTY_GEN())

        generated_examples.extend(self.parser \
                                        .get_definition(self.name, Unit.intent) \
                                        .generate_all(self.variation_name,
                                                      self.arg_value))

        if self.leading_space:
            for (i, ex) in enumerate(generated_examples):
                if may_get_leading_space(ex["text"]):
                    generated_examples[i]["text"] = ' '+ex["text"]
        if self.casegen:
            tmp_buffer = []
            for ex in generated_examples:
                tmp_buffer.append({
                    "text": with_leading_lower(ex["text"]),
                    "entities": ex["entities"],
                })
                tmp_buffer.append({
                    "text": with_leading_upper(ex["text"]),
                    "entities": ex["entities"],
                })
            generated_examples = tmp_buffer
        return generated_examples

    def get_nb_possible_generated_examples(self):
        nb_possible_ex = self.parser.get_definition(self.name, Unit.intent) \
                                    .get_nb_possible_generated_examples(self.variation_name)
        if self.casegen:
            nb_possible_ex *= 2
        if self.randgen is not None:
            nb_possible_ex += 1
        return nb_possible_ex
