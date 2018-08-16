#!/usr/bin/env python3

import re
import os

from utils import *
from parser_utils import *


class Parser():
    """
    This class will parse the input file(s)
    and create an internal representation of its contents.
    """
    def __init__(self, input_file):
        self.in_file = input_file
        self.opened_files = []
        self.line_nb = 0

        self.aliases = dict()  # for each alias, stores a list of list of units
        self.slots = dict()  # for each slot, stores a list of value name and unit
        self.intents = dict()  # for each intent, stores a list of list of slots

        self.parsing_finished = False


    def read_line(self):
        self.line_nb += 1
        return self.in_file.readline()
    def peek_line(self):
        """Returns the next line without moving forward in the file"""
        saved_pos = self.in_file.tell()
        line = self.in_file.readline()
        self.in_file.seek(saved_pos)
        return line

    def is_inside_decl(self):
        next_line = self.peek_line()
        return (next_line.startswith(' ') or next_line.startswith('\t'))


    def parse_file(self, filename):
        """Runs the parsing of the file `filename` within the same parser"""
        self.opened_files.append(self.in_file)
        file_path = os.path.join(os.path.dirname(self.in_file.name), filename)
        with open(file_path, 'r') as in_file:
            self.in_file = in_file
            self.parse()
        self.in_file = self.opened_files.pop()


    def parse(self):
        printDBG("Parsing file: "+self.in_file.name)
        line = None
        while line != "":
            line = self.read_line()
            stripped_line = line.lstrip()
            line_type = get_top_level_line_type(line, stripped_line)

            if line_type == LineType.empty or line_type == LineType.comment:
                continue
            stripped_line = strip_comments(stripped_line)  # Not done before to compute the indentation
            if line_type == LineType.include_file:
                self.parse_file(stripped_line[1:])
            elif line_type == LineType.alias_declaration:
                self.parse_alias_definition(stripped_line)
            elif line_type == LineType.slot_declaration:
                self.parse_slot_definition(stripped_line)
            else:  # intent declaration
                self.parse_intent_definition(stripped_line)

        printDBG("Parsing of file: "+self.in_file.name+" finished")
        self.parsing_finished = True


    def parse_alias_definition(self, first_line):  # Lots of copy-paste in three methods
        """
        Parses the definition of an alias (declaration and contents)
        and adds the relevant info to the list of aliases.
        """
        printDBG("alias: "+first_line.strip())
        # Manage the alias declaration
        (alias_name, alias_precision, randgen, percentgen, casegen) = \
            parse_unit(first_line)
        if randgen is not None:
            raise SyntaxError("Declarations cannot have a named random generation modifier",
                    (self.in_file.name, self.line_nb, 0, line))
        if percentgen is not None:
            raise SyntaxError("Declarations cannot have a random generation modifier",
                    (self.in_file.name, self.line_nb, 0, line))
        if casegen:
            raise SyntaxError("Case generation modifier not accepted in declarations",
                    (self.in_file.name, self.line_nb, indentation_nb, line))

        # Manage the contents
        expressions = []
        indentation_nb = None
        while self.is_inside_decl():
            line = self.read_line()
            stripped_line = line.lstrip()
            indentation_nb = check_indentation(indentation_nb, line, stripped_line)

            expressions.append(split_contents(stripped_line))

        # Put the new definition in the alias dict
        if alias_name in self.aliases:
            if alias_precision is None:
                raise SyntaxError("Found a definition without precision for alias '"
                    +alias_name+"' while another definition was already found",
                    (self.in_file.name, self.line_nb, 0, first_line))
            else:
                self.aliases[alias_name].append({
                    "precision": alias_precision,
                    "expressions": expressions,
                })
        else:
            if alias_precision is None:
                self.aliases[alias_name] = {
                    "expressions": expressions,
                }
            else:
                self.aliases[alias_name] = [{
                    "precision": alias_precision,
                    "expressions": expressions,
                }]

    def parse_slot_definition(self, first_line):
        """
        Parses the definition of a slot (declaration and contents)
        and adds the relevant info to the list of slots.
        """
        printDBG("slot: "+first_line.strip())
        #Manage the slot declaration
        (slot_name, slot_precision, randgen, percentgen, casegen) = \
            parse_unit(first_line)
        if randgen is not None:
            raise SyntaxError("Declarations cannot have a named random generation modifier",
                    (self.in_file.name, self.line_nb, 0, line))
        if percentgen is not None:
            raise SyntaxError("Declarations cannot have a random generation modifier",
                    (self.in_file.name, self.line_nb, 0, line))
        if casegen:
            raise SyntaxError("Case generation modifier not accepted in declarations",
                    (self.in_file.name, self.line_nb, indentation_nb, line))

        #Manage the contents
        expressions = []
        indentation_nb = None
        while self.is_inside_decl():
            line = self.read_line()
            stripped_line = line.lstrip()
            indentation_nb = check_indentation(indentation_nb, line, stripped_line)

            (alt_slot_val_name, expression) = \
                split_contents(stripped_line, accept_alt_solt_val=True)
            expressions.append({
                "slot-value-name": alt_slot_val_name,
                "expression": expression,
            })

        # Put the new definition in the slot dict
        if slot_name in self.slots:
            if slot_precision is None:
                raise SyntaxError("Found a definition without precision for slot '"
                    +slot_name+"' while another definition was already found",
                    (self.in_file.name, self.line_nb, 0, first_line))
            else:
                self.aliases[alias_name].append({
                    "precision": slot_precision,
                    "expressions": expressions,
                })
        else:
            if slot_precision is None:
                self.slots[slot_name] = {
                    "expressions": expressions,
                }
            else:
                self.slots[slot_name] = [{
                    "precision": slot_precision,
                    "expressions": expressions,
                }]

    def parse_intent_definition(self, first_line):
        """
        Parses the definition of an intent (declaration and contents)
        and adds the relevant info to the list of intents.
        """
        printDBG("intent: "+first_line.strip())
        # Manage the intent declaration
        (intent_name, intent_precision, randgen, percentgen, casegen) = \
            parse_unit(first_line)
        if randgen is not None:
            raise SyntaxError("Declarations cannot have a named random generation modifier",
                    (self.in_file.name, self.line_nb, 0, line))
        if percentgen is not None:
            raise SyntaxError("Declarations cannot have a random generation modifier",
                    (self.in_file.name, self.line_nb, 0, line))
        if casegen:
            raise SyntaxError("Case generation modifier not accepted in declarations",
                    (self.in_file.name, self.line_nb, indentation_nb, line))
        nb_gen_asked = find_nb_gen_asked(first_line)

        # Manage the contents
        expressions = []
        indentation_nb = None
        while self.is_inside_decl():
            line = self.read_line()
            stripped_line = line.lstrip()
            indentation_nb = check_indentation(indentation_nb, line, stripped_line)

            expressions.append(split_contents(stripped_line))

        # Put the new definition in the intent dict
        if intent_name in self.intents:
            if intent_precision is None:
                raise SyntaxError("Found a definition without precision for intent '"
                    +intent_name+"' while another definition was already found",
                    (self.in_file.name, self.line_nb, 0, first_line))
            else:
                self.intents[intent_name].append({
                    "nb-gen-asked": nb_gen_asked,
                    "precision": intent_precision,
                    "expressions": expressions,
                })
        else:
            if intent_precision is None:
                self.intents[intent_name] = {
                    "nb-gen-asked": nb_gen_asked,
                    "expressions": expressions,
                }
            else:
                self.intents[intent_name] = [{
                    "nb-gen-asked": nb_gen_asked,
                    "precision": intent_precision,
                    "expressions": expressions,
                }]


    def has_parsed(self):
        return self.parsing_finished


    def printDBG(self):
        print("\nAliases:")
        for name in self.aliases:
            current_alias_def = self.aliases[name]
            print("\t"+name+": ")
            if isinstance(current_alias_def, list):
                for precised_def in current_alias_def:
                    print("\t\tprecision: "+precised_def["precision"])
                    for expr in precised_def["expressions"]:
                        print("\t\t\texpression: "+str(expr))
            else:
                for expr in current_alias_def["expressions"]:
                    print("\t\texpression: "+str(expr))

        print("\nSlots:")
        for name in self.slots:
            current_slot_def = self.slots[name]
            print("\t"+name+": ")
            if isinstance(current_slot_def, list):
                for precised_def in current_slot_def:
                    print("\t\tprecision: "+precised_def["precision"])
                    for expr in precised_def["expressions"]:
                        print("\t\t\texpression: "+str(expr))
            else:
                for expr in current_slot_def["expressions"]:
                    print("\t\texpression: "+str(expr))

        print("\nIntents:")
        for name in self.intents:
            current_intent_def = self.intents[name]
            if isinstance(current_intent_def, list):
                print("\t"+name+":")
                for precised_def in current_intent_def:
                    print("\t\tprecision: "+precised_def["precision"]
                        +" to generate "+str(precised_def["nb-gen-asked"])+"x")
                    for expr in precised_def["expressions"]:
                        print("\t\t\texpression: "+str(expr))
            else:
                print("\t"+name+"(to generate "
                    +str(current_intent_def["nb-gen-asked"])+"x): ")
                for expr in current_intent_def["expressions"]:
                    print("\t\texpression: "+str(expr))


if __name__ == "__main__":
    import warnings
    warnings.warn("You are running the wrong file ('Parser.py')." +
        "The file that should be run is 'main.py'.")
