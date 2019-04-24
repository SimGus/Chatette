from __future__ import print_function

from chatette.units import Example, RuleContent, may_get_leading_space, \
                           randomly_change_case, with_leading_lower, with_leading_upper
from chatette.utils import choose
from chatette.parsing.parser_utils import add_escapement_back_in_choice_item, \
                                          CHOICE_SEP


class ChoiceRuleContent(RuleContent):
    """
    This class represents a choice as it can be contained in a rule,
    with its modifiers.
    Accepted modifiers:
        - leading-space: bool
        - casegen: bool
        - randgen: str
        # TODO: maybe more?
    """

    def __init__(self, name, leading_space=False, variation_name=None,
                 arg_value=None, casegen=False, randgen=None, percentage_gen=None,
                 parser=None):
        # NOTE: its name would be the unparsed text as a string
        if randgen is not None and randgen != "" and type(randgen) != bool:
            raise SyntaxError("Choices cannot have a named randgen, " +
                              "as was the case for '" + name + "': " + randgen +
                              " ('?' unescaped?)")
        if variation_name is not None:
            raise SyntaxError("Choices cannot have a variation, as was the " +
                              "case for '" + name + "' ('#' unescaped?)")
                              # TODO: change the symbol to a variable from parser_utils
        if arg_value is not None:
            raise SyntaxError("Choices cannot have an argument, as was the " +
                              "case for '" + name + "' ('$' unescaped?)")
        if percentage_gen is not None:
            raise SyntaxError("Choices cannot have an percentage for random " +
                              "generation, as was the case for '" + name + "'.")

        if randgen is None:
            randgen = False

        super(ChoiceRuleContent, self).__init__(
            name,
            leading_space=leading_space,
            variation_name=None,
            arg_value=None,
            casegen=casegen,
            randgen=randgen,
            percentage_gen=None,
            parser=None)

        self.choices = []
        self.casegen_checked = False


    def can_have_casegen(self):
        for choice in self.choices:
            if len(choice) > 0 and choice[0].can_have_casegen():
                return True
        return False

    def check_casegen(self):
        """Checks that casegen is applicable (at generation time)."""
        if not self.casegen_checked and self.casegen:
            if not self.can_have_casegen():
                self.casegen = False
            self.casegen_checked = True

    def get_max_nb_generated_examples(self):
        nb_possible_ex = 0
        for choice in self.choices:
            choice_nb_ex = 0
            for token in choice:
                current_nb_ex = token.get_max_nb_generated_examples()
                if choice_nb_ex == 0:
                    choice_nb_ex = current_nb_ex
                else:
                    choice_nb_ex *= current_nb_ex
            nb_possible_ex += choice_nb_ex

        if self.casegen:
            nb_possible_ex *= 2
        if self.randgen:
            nb_possible_ex += 1
        return nb_possible_ex


    def add_choice(self, choice):
        # ([RuleContent]) -> ()
        if len(choice) <= 0:
            return
        self.choices.append(choice)

    def add_choices(self, choices):
        # ([[RuleContent]]) -> ()
        interesting_choices = [choice for choice in choices if len(choice) > 0]
        if len(interesting_choices) <= 0:
            return
        self.choices.extend(interesting_choices)


    def generate_random(self, generated_randgens=None):
        if generated_randgens is None:
            generated_randgens = dict()

        self.check_casegen()

        # Manage randgen
        if self.randgen:
            return Example()

        if len(self.choices) <= 0:
            return Example()

        choice = choose(self.choices)
        generated_example = Example()

        for token in choice:
            generated_token = token.generate_random(generated_randgens)
            generated_example.text += generated_token.text
            generated_example.entities.extend(generated_token.entities)

        if self.casegen:
            generated_example.text = randomly_change_case(generated_example.text)
        if self.leading_space and may_get_leading_space(generated_example.text):
            generated_example.text = ' ' + generated_example.text

        return generated_example

    def generate_all(self):
        self.check_casegen()

        generated_examples = []
        if self.randgen:
            generated_examples.append(Example())

        for choice in self.choices:
            current_examples = []
            for token in choice:
                current_token_all_generations = token.generate_all()
                if len(current_examples) <= 0:
                    current_examples = [gen for gen in current_token_all_generations]
                else:
                    current_examples = [
                        Example(
                            partial_example.text + gen.text,
                            partial_example.entities + gen.entities
                        )
                        for partial_example in current_examples
                        for gen in current_token_all_generations]
            generated_examples.extend(current_examples)

        if self.leading_space:
            for (i, ex) in enumerate(generated_examples):
                if may_get_leading_space(ex.text):
                    generated_examples[i].text = ' ' + ex.text

        if self.casegen:
            tmp_buffer = []
            for ex in generated_examples:
                tmp_buffer.append(Example(with_leading_lower(ex.text), ex.entities))
                tmp_buffer.append(Example(with_leading_upper(ex.text), ex.entities))

        return generated_examples


    def print_DBG(self, nb_indent=0):
        indentation = nb_indent * '\t'
        print(indentation + self.name)
        print(indentation + "\tvariation name: " + str(self.variation_name))
        print(indentation + "\targ value: " + str(self.arg_value))
        print(indentation + "\tcasegen: " + str(self.casegen))
        print(indentation + "\trandgen: " + str(self.randgen) + " with percentage: "
              + str(self.percentgen))

        for choice in self.choices:
            print(indentation + "\tChoice:")
            for token in choice:
                token.print_DBG(nb_indent + 2)

    def as_string(self):
        """
        Returns the representation of the rule
        as it would be written in a template file.
        """
        result = ""
        for choice in self.choices:
            if result != "":
                result += CHOICE_SEP
            for sub_rule in choice:
                result += \
                    add_escapement_back_in_choice_item(sub_rule.as_string())
        if self.casegen:
            result = '&'+result
        if self.variation_name is not None:
            result += '#'+self.variation_name
        if self.randgen:
            result += '?'
            if self.percentgen != 50:
                result += '/'+str(self.percentgen)
        if self.arg_value is not None:
            result += '$'+self.arg_value
        result = '{' + result + '}'
        if self.leading_space:
            result = ' '+result
        return result
