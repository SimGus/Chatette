from random import randint

from chatette.parsing.parser_utils import UnitType, \
                                          add_escapement_back_in_unit_ref
from chatette.units import Example, RuleContent, may_get_leading_space, \
                           may_change_leading_case, randomly_change_case, \
                           with_leading_lower, with_leading_upper


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
        # TODO replace parser by self definition
        super(AliasRuleContent, self).__init__(name, leading_space=leading_space,
                                               variation_name=variation_name,
                                               arg_value=arg_value, casegen=casegen,
                                               randgen=randgen, percentage_gen=percentage_gen,
                                               parser=parser)
        self.casegen_checked = False


    def get_max_nb_generated_examples(self):
        nb_possible_ex = self.parser.get_definition(self.name, UnitType.alias) \
            .get_max_nb_generated_examples(self.variation_name)
        if self.casegen:
            nb_possible_ex *= 2
        if self.randgen is not None:
            nb_possible_ex += 1
        return nb_possible_ex

    def can_have_casegen(self):
        return self.parser.get_definition(self.name, UnitType.alias) \
            .can_have_casegen()

    def check_casegen(self):
        """Checks that casegen is applicable (at generation time)."""
        if not self.casegen_checked and self.casegen:
            if not self.can_have_casegen():
                self.casegen = False
            self.casegen_checked = True


    def generate_random(self, generated_randgens=None):
        if generated_randgens is None:
            generated_randgens = dict()

        self.check_casegen()

        # Manage randgen
        if self.randgen is not None and self.randgen in generated_randgens:
            if generated_randgens[self.randgen]:
                pass  # Must be generated
            else:
                return Example()  # Cannot be generated
        elif self.randgen is not None:
            if randint(0, 99) >= self.percentgen:
                # Don't generated this randgen
                if self.randgen != "":
                    generated_randgens[self.randgen] = False
                return Example()
            elif self.randgen != "":
                # Generate this randgen
                generated_randgens[self.randgen] = True

        generated_example = self.parser.get_definition(self.name, UnitType.alias) \
            .generate_random(self.variation_name, self.arg_value)

        if self.casegen:
            generated_example.text = \
                randomly_change_case(generated_example.text)

        if self.leading_space and may_get_leading_space(generated_example.text):
            generated_example.text = ' ' + generated_example.text

        return generated_example

    def generate_all(self):
        self.check_casegen()

        generated_examples = []
        if self.randgen is not None:
            generated_examples.append(Example())

        aliases = self.parser \
                      .get_definition(self.name, UnitType.alias) \
                      .generate_all(self.variation_name, self.arg_value)

        generated_examples.extend(aliases)

        if self.leading_space:
            for (i, ex) in enumerate(generated_examples):
                if may_get_leading_space(ex.text):
                    generated_examples[i].text = ' ' + ex.text
        if self.casegen:
            tmp_buffer = []
            for ex in generated_examples:
                if may_change_leading_case(ex.text):
                    tmp_buffer.append(Example(with_leading_lower(ex.text), ex.entities))
                    tmp_buffer.append(Example(with_leading_upper(ex.text), ex.entities))
                else:
                    tmp_buffer.append(ex)
            generated_examples = tmp_buffer
        return generated_examples


    def as_string(self):
        """
        Returns the representation of the rule
        as it would be written in a template file.
        """
        result = add_escapement_back_in_unit_ref(self.name)
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
        result = "~[" + result + ']'
        if self.leading_space:
            result = ' '+result
        return result
