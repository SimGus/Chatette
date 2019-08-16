# coding: utf-8
"""
Module `chatette.refactor_units.modifiable.definitions.unit_definition`
Contains the abstract class that is base for all unit definitions.
"""

from random import choice

from chatette.refactor_units.modifiable import ModifiableItem


class UnitDefinition(ModifiableItem):
    """Abstract class base for all unit definitions."""
    def __init__(self, identifier, modifiers):
        super(UnitDefinition, self).__init__(
            identifier, False, modifiers  # NOTE `False` corresponds to `leading_space`
        )
        self.identifier = identifier
        self._rules = []

    def _compute_nb_possibilities(self):
        acc = 0
        for rule in self._rules:
            acc += rule.get_max_nb_possibilities()
        return acc
    
    def add_rule(self, rule):
        """Adds the rule `rule` to the list of rules."""
        self._rules.append(rule)
    def add_rules(self, rules):
        """Adds each of the rules `rule` to the list of rules."""
        self._rules.extend(rules)
    
    def remove_rule(self, index):
        """Removes the rule at `index`th rule."""
        if index < 0 or index >= len(self._rules):
            raise ValueError("Tried to remove rule at invalid index.")
        del self._rule[index]
    
    def _choose_rule(self):
        """
        Returns a rule at random from the list of rules for this definition.
        Returns `None` if there are no rules.
        """
        if len(self._rules) == 0:
            return None
        return choice(self._rules)

    def _generate_random_strategy(self):
        rule = self._choose_rule()
        if rule is None:
            raise SyntaxError(
                self.full_name.capitalize() + " does not have any rule to " + \
                "generate."
            )
        
        return rule.generate_random()
    
    def _generate_all_strategy(self):
        generated_examples = []
        for rule in self._rules:
            current_examples = rule.generate_all()
            generated_examples.extend(current_examples)
        return generated_examples
    