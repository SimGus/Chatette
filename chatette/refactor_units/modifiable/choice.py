# coding: utf-8
"""
Module `chatette.refactor_units.modifiable.choice`
Contains the class that represents choices (and old word groups).
"""

from random import choice

from chatette.refactor_units.modifiable import ModifiableItem


class Choice(ModifiableItem):
    """
    Represents a choice that can choose between rules and generate one of them.
    """
    def __init__(self, name, leading_space, modifiers, rules=None):  # TODO fix the problem that choice have no by design name
        super(Choice, self).__init__(name, leading_space, modifiers)
        self._rules = []
        if rules is not None:
            print("choice rules: " + str(rules))
            self._rules.extend(rules)

    def _compute_full_name(self):
        return "choice '" + self._name + "'"
    
    def _compute_nb_possibilities(self):
        acc = 0
        for rule in self._rules:
            print("for rule " + str(rule.full_name) + " max: " + str(rule.get_max_nb_possibilities()))
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
