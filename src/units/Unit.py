#!/usr/bin/env python3

from random import randint

from Generator import randomly_change_case


class UnitDefinition():
    """Superclass representing a unit definition"""
    def __init__(self, name, rules=[], arg=None, casegen=False):
        self.type = "unit"

        self.name = name
        self.rules = rules
        self.argument_identifier = arg

        self.variations = dict()

        self.casegen = casegen


    def add_rule(self, rule, variation_name=None):
        if variation_name is None:
            self.rules.append(rule)
        else:
            if variation_name == "":
                raise SyntaxError("Defining a "+self.type+" with an empty name"+
                    "is not allowed")
            if variation_name not in self.variations:
                self.variations[variation_name] = [rule]
            else:
                self.variations[variation_name].append(rule)
            self.rules.append(rule)

    def generate_random(self, variation_name=None, arg_value=None):
        """
        Generates one of your rule at random and
        returns the string generated and the entities inside it
        """
        chosen_rule = None
        if variation_name is None:
            chosen_rule = self.rules[randint(0,len(self.rules)-1)]
        else:
            if variation_name not in self.variations:
                raise SyntaxError("Couldn't find a variation named '"+
                    variation_name+"' for "+self.type+" '"+self.name+"'")
            chosen_rule = \
                self.rules[randint(0, len(self.variations[variation_name])-1)]
        (text, entities) = chosen_rule.generate(arg_value)
        if self.casegen:
            text = randomly_change_case(text)
        return (text, entities)

    def generate_all(self):
        pass  # TODO
