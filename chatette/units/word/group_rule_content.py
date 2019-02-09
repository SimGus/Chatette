from random import randint

from chatette.units import Example, RuleContent, may_change_leading_case, \
                           may_get_leading_space, randomly_change_case, \
                           with_leading_lower, with_leading_upper
from chatette.parsing.parser_utils import add_escapement_back_in_group


class GroupWordRuleContent(RuleContent):
    """
    Represents a word group token inside a rule.
    `name` is actually the words as a string.
    Accepted modifiers:
        - leading-space: bool
        - casegen: bool
        - randgen: str
        - percentgen: bool
    """

    def __init__(self, name, leading_space=False, variation_name=None, arg_value=None,
                 casegen=False, randgen=None, percentage_gen=50, parser=None):
        if variation_name is not None:
            raise SyntaxError("Word groups cannot have variations, yet '" +
                              name + "' does (unescaped '#'?)")
        if arg_value is not None:
            raise SyntaxError("Word groups cannot have an argument, yet '" +
                              name + "' does (unescaped '$'?)")
        if parser is not None:
            raise RuntimeError("Internal error: tried to create a word " +
                               "group with a pointer to the parser")

        if not may_change_leading_case(name):
            casegen = False

        super(GroupWordRuleContent, self).__init__(name,
                                                   leading_space=leading_space,
                                                   variation_name=None,
                                                   arg_value=None,
                                                   casegen=casegen,
                                                   randgen=randgen,
                                                   percentage_gen=percentage_gen,
                                                   parser=None)
        self.words = name

    def can_have_casegen(self):
        return may_change_leading_case(self.words)

    def generate_random(self, generated_randgens=None):
        if generated_randgens is None:
            generated_randgens = dict()

        if self.randgen is not None and self.randgen in generated_randgens:
            if generated_randgens[self.randgen]:
                pass  # Must be generated
            else:
                return Example()  # Cannot be generated
        elif self.randgen is not None:
            if randint(0, 99) >= self.percentgen:
                # Don't generated this randgen
                generated_randgens[self.randgen] = False
                return Example()
            else:
                # Generate this randgen
                generated_randgens[self.randgen] = True

        # Generate the string according to the parameters of the object
        generated_str = self.words
        if self.casegen:
            generated_str = randomly_change_case(generated_str)

        if self.leading_space and may_get_leading_space(generated_str):
            generated_str = ' ' + generated_str

        return Example(generated_str)

    def generate_all(self):
        generated_examples = []
        if self.randgen is not None:
            generated_examples.append("")

        if self.casegen:
            generated_examples.append(with_leading_lower(self.words))
            generated_examples.append(with_leading_upper(self.words))
        else:
            generated_examples.append(self.words)

        if self.leading_space:
            for (i, ex) in enumerate(generated_examples):
                if may_get_leading_space(ex):
                    generated_examples[i] = ' ' + ex

        result = [Example(ex) for ex in generated_examples]
        return result

    def get_max_nb_generated_examples(self):
        nb_possible_ex = 1
        if self.casegen:
            nb_possible_ex *= 2
        if self.randgen is not None:
            nb_possible_ex += 1
        return nb_possible_ex

    def as_string(self):
        """
        Returns the representation of the rule
        as it would be written in a template file.
        """
        result = add_escapement_back_in_group(self.name)
        if self.casegen:
            result = '&'+result
        if self.variation_name is not None:
            result += '#'+self.variation_name
        if self.randgen is not None:
            result += '?'+str(self.randgen)
            if self.percentgen != 50:
                result += '/'+str(self.percentgen)
        if self.arg_value is not None:
            result += '$'+self.arg_value
        result = '[' + result + ']'
        if self.leading_space:
            result = ' '+result
        return result
