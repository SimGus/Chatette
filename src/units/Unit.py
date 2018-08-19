#!/usr/bin/env python3

from random import randint


class UnitDefinition():
    """Super class representing a unit definition"""
    def __init__(self, name, rules=[], casegen=False, randgen=False,
        randgen_id=None, randgen_percentage=None):
            self.type = "unit"

            self.name = name
            self.rules = rules

            self.variations = dict()

            self.casegen = casegen
            self.randgen = randgen
            self.randgen_id = randgen_id
            self.randgen_percentage = randgen_percentage

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

    def generate_random(self, variation_name=None):
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
        return chosen_rule.generate()
    def generate_all(self):
        pass  # TODO
