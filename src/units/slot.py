from .units import *


class SlotDefinition(UnitDefinition):
    """
    This class represents the definition of a slot,
    containing all the rules that it could generate.
    """
    def __init__(self, name, rules=[], arg=None, casegen=False):
        super(SlotDefinition, self).__init__(name, rules=rules, arg=arg,
            casegen=casegen)
        self.type = "alias"

    # Everything else is in the superclass


class SlotRule(Rule):
    """
    This class represents a slot as it can be contained in a rule,
    with its modifiers.
    Accepted modifiers:
        - leading-space: bool
        - casegen: bool
        - randgen: str
        - percentgen: int
        - arg: str
        - variation-name: str
        - slot-val: str (to define later)
    """
    def __init__(self, name, leading_space=False, variation_name=None, arg_value=None,
        casegen=False, randgen=None, percentage_gen=50, parser=None):
            super(SlotRule, self).__init__(name, leading_space=leading_space,
                variation_name=variation_name, arg_value=arg_value, casegen=casegen,
                percentage_gen=percentage_gen, parser=parser)
            self.slot_value = None  # The generated slot value will be the generated text

    def set_slot_value(self, slot_value):
        # str -> ()
        self.slot_value = slot_value


    def generate_random(self):
        if self.randgen is not None and randint(0,99) >= self.percentgen:
            return EMPTY_GEN  # TODO keep track of which randgen have been generated

        generated_example = self.parser.get_definition(self.name, Unit.slot)\
                                       .generate_random(self.variation_name, \
                                                        self.arg_value)

        if self.casegen:
            generated_example["text"] = \
                randomly_change_case(generated_example["text"])
        if self.leading_space:
            generated_example["text"] = ' '+generated_example["text"]
        return generated_example

    def generate_all(self):
        generated_examples = []
        if randgen is not None:
            generated_examples.append(EMPTY_GEN)

        generated_examples.extend(self.parser.get_definition(self.name, Unit.slot) \
                                             .generate_all(self.arg_value))

        if self.leading_space:
            for (i, ex) in enumerate(generated_examples):
                generated_examples[i]["text"] = ' '+ex["text"]
        if self.casegen:
            tmp_buffer = []
            for ex in generated_examples:
                tmp.buffer.append({
                    "text": with_leading_lower(ex["text"]),
                    "entities": ex["entities"],
                })
                tmp.buffer.append({
                    "text": with_leading_upper(ex["text"]),
                    "entities": ex["entities"],
                })
        return generated_examples
