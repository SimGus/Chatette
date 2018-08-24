from .units import *
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
        self.nb_examples_asked = None  # All possibilities will be generated TODO

    def set_nb_examples(self, nb_examples_asked):
        # int -> ()
        self.nb_examples_asked = nb_examples_asked


    def generate(self):
        """
        Generates all the examples that were asked (i.e. as much examples
        as asked). The number of generated examples is tied to a maximum though.
        """
        if self.nb_examples_asked is None:
            print("No number of examples given not yet supported")
            return []

        generated_examples = []
        for _ in range(self.nb_examples_asked):
            # TODO check that this example hasn't been generated already
            current_example = self.generate_random()
            current_example["text"] = current_example["text"].strip()  # Strip for safety
            generated_examples.append(current_example)
        return generated_examples

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

    def generate_random(self, generated_randgens=dict()):
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
        generated_examples = []
        if self.randgen is not None:
            generated_examples.append(EMPTY_GEN())

        generated_examples.extend(self.parser.get_definition(self.name, Unit.intent) \
                                             .generate_all(self.arg_value))

        if self.leading_space:
            for (i, ex) in enumerate(generated_examples):
                if may_get_leading_space(ex["text"]):
                    generated_examples[i]["text"] = ' '+ex["text"]
        if self.casegen:
            tmp_buffer = []
            for ex in generated_examples:  # TODO: list comprehension
                tmp.buffer.append({
                    "text": with_leading_lower(ex["text"]),
                    "entities": ex["entities"],
                })
                tmp.buffer.append({
                    "text": with_leading_upper(ex["text"]),
                    "entities": ex["entities"],
                })
            generated_examples = tmp_buffer
        return generated_examples
