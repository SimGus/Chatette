from __future__ import print_function
from random import randint

from chatette.parsing.parser_utils import UnitType, remove_escapement, \
                                          add_escapement_back_in_unit_ref
from chatette.units import Example, RuleContent, may_get_leading_space, \
                           may_change_leading_case, randomly_change_case, \
                           with_leading_lower, with_leading_upper


class SlotRuleContent(RuleContent):
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
        super(SlotRuleContent, self).__init__(name, leading_space=leading_space,
                                              variation_name=variation_name,
                                              arg_value=arg_value, casegen=casegen,
                                              randgen=randgen, percentage_gen=percentage_gen,
                                              parser=parser)
        self.casegen_checked = False


    def can_have_casegen(self):
        return self.parser.get_definition(self.name, UnitType.slot) \
            .can_have_casegen()

    def check_casegen(self):
        """Checks that casegen is applicable (at generation time)."""
        if not self.casegen_checked and self.casegen:
            if not self.can_have_casegen():
                self.casegen = False
            self.casegen_checked = True

    def get_max_nb_generated_examples(self):
        nb_possible_ex = self.parser.get_definition(self.name, UnitType.slot) \
            .get_max_nb_generated_examples(self.variation_name)

        if self.casegen:
            nb_possible_ex *= 2
        if self.randgen is not None:
            nb_possible_ex += 1
        return nb_possible_ex


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

        generated_example = self.parser.get_definition(self.name, UnitType.slot) \
            .generate_random(self.variation_name, self.arg_value)

        if self.casegen:
            generated_example.text = randomly_change_case(generated_example.text)

        if self.leading_space and may_get_leading_space(generated_example.text):
            generated_example.text = ' ' + generated_example.text

        return generated_example

    def generate_all(self):
        self.check_casegen()

        generated_examples = []
        if self.randgen is not None:
            generated_examples.append(Example())

        slots = self.parser.get_definition(self.name, UnitType.slot) \
            .generate_all(self.variation_name, self.arg_value)

        generated_examples.extend(slots)

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
        result = "@[" + result + ']'
        if self.leading_space:
            result = ' '+result
        return result


class DummySlotValRuleContent(RuleContent):
    """
    This class is supposed to be the first rule inside a list of rules that has
    a slot value. It won't generate anything ever.
    `self.name` and `self.slot_value` map to the slot value it represents.
    """

    def __init__(self, name, next_token):
        # (str, RuleContent) -> ()
        super(DummySlotValRuleContent, self).__init__(name)
        self.name = remove_escapement(name)
        self.slot_value = self.name
        self.real_first_token = next_token

    def can_have_casegen(self):
        return self.real_first_token.can_have_casegen()

    def generate_random(self, generated_randgens=None):
        return Example()

    def generate_all(self):
        return [Example()]

    def print_DBG(self, nb_indent=0):
        indentation = nb_indent * '\t'
        print(indentation + "Slot val: " + self.name)

    def as_string(self):
        return ""
