from .units import *
from parser_utils import Unit


class AliasDefinition(UnitDefinition):
    """
    This class represents the definition of an alias,
    containing all the rules that it can represent.
    """
    def __init__(self, name, rules=[], arg=None, casegen=False):
        super(AliasDefinition, self).__init__(name, rules=rules, arg=arg,
            casegen=casegen)
        self.type = "alias"

    # Everything else is in the superclass


class AliasRuleContent(RuleContent):
    """
    This class represents an alias as it can be contained in a rule,
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
            super(AliasRuleContent, self).__init__(name, leading_space=leading_space,
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

        generated_example = self.parser.get_definition(self.name, Unit.alias) \
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
            generated_examples.append(EMPTY_GEN())

        generated_examples.extend(self.parser.get_definition(self.name, Unit.alias) \
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
