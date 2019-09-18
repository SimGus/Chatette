# coding: utf-8
"""
Module `chatette.units.modifiable.definitions.unit_definition`
Contains the abstract class that is base for all unit definitions.
"""

from random import choice
from copy import deepcopy

from chatette.utils import UnitType
from chatette.units.modifiable import ModifiableItem
from chatette.units import extend_no_dup

from chatette.parsing.utils import SLOT_VAL_FIRST_RULE
from chatette.parsing import utils as putils

from chatette.statistics import Stats


class UnitDefinition(ModifiableItem):
    """Abstract class base for all unit definitions."""
    unit_type = None
    def __init__(self, identifier, modifiers):
        super(UnitDefinition, self).__init__(
            identifier, False, modifiers  # NOTE `False` corresponds to `leading_space`
        )
        self.identifier = identifier
        self._all_rules = []
        self._variation_rules = dict()
    
    
    def __contains__(self, variation_name):
        """
        Returns `True` if `variation_name` is a variation
        that is declared for the current definition.
        """
        return (variation_name in self._variation_rules)


    def set_identifier(self, new_identifier):
        """
        Changes the identifier of the current unit and recomputes its full name.
        @pre: `new_identifier` wasn't already in use for another unit of the
              same type.
        """
        self.identifier = new_identifier
        self._name = new_identifier
        self.full_name = self._compute_full_name()


    def _compute_nb_possibilities(self, variation_name=None):
        if variation_name is None:
            relevant_rules = self._all_rules
        elif variation_name in self._variation_rules:
            relevant_rules = self._variation_rules[variation_name]
        else:
            raise SyntaxError(
                "Referenced variation '" + str(variation_name) + "' for " + \
                self.full_name + ", but this variation has no rules " + \
                "associated to it."
            )

        acc = 0
        for rule in relevant_rules:
            acc += rule.get_max_nb_possibilities()
        return acc


    def _check_rule_validity(self, rule):
        """Raises a `ValueError` if the rule `rule` is not valid."""
        if rule.slot_value is not None:
            raise ValueError(
                "One of the rules in " + self.full_name + " was not valid: " + \
                "it contained a slot value. The invalid rule is " + str(rule)
            )
    
    def add_rule(self, rule, variation_name=None):
        """
        Adds the rule `rule` to the list of rules.
        If `variation_name` is not `None`, adds the rule to the corresponding
        variation.
        @raises: `ValueError` if `rule` is not valid.
        """
        self._check_rule_validity(rule)
        if variation_name in self._variation_rules:
            self._variation_rules[variation_name].append(rule)
        else:
            self._variation_rules[variation_name] = [rule]
        self._all_rules.append(rule)
    def add_all_rules(self, rules, variation_name=None):
        """
        Adds each of the rules `rule` to the list of rules.
        If `variation_name` is not `None`, adds the rules to the corresponding
        variation.
        @raises: `ValueError` if one of the rules in `rules` is not valid.
        """
        for rule in rules:
            self._check_rule_validity(rule)
        if variation_name in self._variation_rules:
            self._variation_rules[variation_name].extend(rule)
        else:
            self._variation_rules[variation_name] = rules
        self._all_rules.extend(rules)
    
    def _recompute_all_rules(self):
        """
        Given all the rules in `self._variation_rules`,
        recomputes all the possible rules and put them in `self._all_rules`.
        """
        all_rules = []
        for rules in self._variation_rules:
            all_rules.extend(rules)
        self._all_rules = all_rules
    
    def remove_rule(self, index, variation_name=None):
        """Removes the rule at `index`th rule."""
        # TODO decide what to do with `variation_name`
        if index < 0 or index >= len(self._all_rules):
            raise ValueError("Tried to remove rule at invalid index.")
        del self._rule[index]
    

    def _choose_rule(self, variation_name=None):
        """
        Returns a rule at random from the list of rules for this definition.
        Returns `None` if there are no rules.
        If `variation_name` is not `None`, the rule chosen should come
        from the corresponding variation (if it exists).
        """
        if variation_name is None:
            if len(self._all_rules) == 0:
                return None
            return choice(self._all_rules)
        else:
            if (
                variation_name not in self._variation_rules
                or len(self._variation_rules[variation_name]) == 0
            ):
                return None
            return choice(self._variation_rules[variation_name])


    def has_variation(self, variation_name):
        """Returns `True` iff `variation_name` was declared for this unit."""
        return (variation_name in self._variation_rules)
    def get_number_variations(self):
        if None in self._variation_rules:
            return len(self._variation_rules) - 1
        return len(self._variation_rules)
    def delete_variation(self, variation_name):
        """
        Deletes the variation named `variation_name`.
        @raises: - `KeyError` if the variation doesn't exist.
        """
        if not self.has_variation(variation_name):
            raise KeyError(
                "Tried to delete variation '" + str(variation_name) + \
                "' of " + self.full_name + ", but it wasn't defined."
            )
        Stats.get_or_create().one_variation_unit_removed(self.unit_type)
        del self._variation_rules[variation_name]
        self._recompute_all_rules()


    def _generate_random_strategy(self, variation_name=None):
        rule = self._choose_rule(variation_name)
        if rule is None:
            if variation_name is None:
                raise SyntaxError(
                    self.full_name.capitalize() + " does not have any rule to " + \
                    "generate."
                )
            else:
                raise SyntaxError(
                    self.full_name.capitalize() + " does not have any rule " + \
                    "associated to variation '" + str(variation_name) + "'."
                )
        
        example = rule.generate_random()
        example.remove_leading_space()
        if self.unit_type == UnitType.slot:
            example._slot_value = rule.slot_value
            if (
                example._slot_value is not None
                and example._slot_value.strip() == SLOT_VAL_FIRST_RULE
            ):
                if len(rule._contents) == 0:
                    raise SyntaxError(
                        "The slot value given for one of the rules of " + \
                        self.full_name + " references the first token of " + \
                        "an empty rule."
                    )
                example._slot_value = rule._contents[0]._name
        return example


    def generate_all(self, variation_name=None):
        """Overriding to prevent caching of examples for just one variation."""
        if not self._variation_rules:
            return super(UnitDefinition, self).generate_all()
        
        if isinstance(self._cached_examples, list):
            self._cached_examples = dict()
        if variation_name not in self._cached_examples:
            basic_examples = \
                self._generate_all_strategy(variation_name=variation_name)
            if self._leading_space:
                for ex in basic_examples:
                    ex.prepend(' ')
            self._cached_examples[variation_name] = \
                self._apply_modifiers_to_all(basic_examples)
        return deepcopy(self._cached_examples[variation_name])

    
    def _generate_all_strategy(self, variation_name=None):
        if variation_name is None:
            relevant_rules = self._all_rules
        elif variation_name in self._variation_rules:
            relevant_rules = self._variation_rules[variation_name]
        else:
            raise SyntaxError(
                "Tried to generate examples for variation '" + \
                str(variation_name) + "' of " + self.full_name + \
                ", but this variation has no rules associated to it."
            )

        generated_examples = []
        for rule in relevant_rules:
            current_examples = rule.generate_all()
            if self.unit_type == UnitType.slot:
                for ex in current_examples:
                    ex._slot_value = rule.slot_value
                    if (
                        ex._slot_value is not None
                        and ex._slot_value.strip() == SLOT_VAL_FIRST_RULE
                    ):
                        if len(rule._contents) == 0:
                            raise SyntaxError(
                                "The slot value given for one of the rules " + \
                                "of " + self.full_name + \
                                " references the first token of an empty rule."
                            )
                        ex._slot_value = rule._contents[0]._name
            for ex in current_examples:
                ex.remove_leading_space()
            generated_examples = \
                extend_no_dup(generated_examples, current_examples)
        return generated_examples
    

    def short_description(self):
        """
        Returns a short description (as a `str`) that can be displayed to the
        user.
        """
        desc = self.full_name + "\n"
        desc += self._modifiers_repr.short_description()
        if None in self._variation_rules:
            desc += str(max(0, len(self._variation_rules) - 1)) + " variation(s)"
        else:
            desc += str(len(self._variation_rules)) + " variation(s)"
        if len(self._variation_rules) > 1:
            desc += ':'
        for (i, variation_name) in enumerate(self._variation_rules):
            if variation_name is None:
                continue
            desc += "\n\t- " + variation_name
            if i >= 12:
                desc += "\n\t- ..."
                break
        return desc

    def as_template_str(self):
        result = ""
        for variation_name in self._variation_rules:
            result += putils.get_template_unit_sym(self.unit_type)
            result += putils.UNIT_START_SYM
            result += putils.get_template_pre_modifiers(self._modifiers_repr)
            result += self._name
            result += putils.get_template_post_modifiers(self._modifiers_repr)
            if variation_name is not None:
                result += putils.VARIATION_SYM + variation_name
            result += putils.UNIT_END_SYM

            for rule in self._variation_rules[variation_name]:
                result += '\n\t' + rule.as_template_str()
        return result
    