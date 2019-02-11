"""
Module `chatette.cli.interactive_commands.declare_command`.
Contains the strategy class that represents the interactive mode command
`declare` which creates a new empty unit and add it to the list of units
of the parser.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.parsing.parser_utils import UnitType
from chatette.units.alias.definition import AliasDefinition
from chatette.units.slot.definition import SlotDefinition
from chatette.units.intent.definition import IntentDefinition


class DeclareCommand(CommandStrategy):
    usage_str = 'declare <unit-type> "<unit-name>"'

    def execute(self, facade):
        """
        Implements the command `rule` which generates a certain number of
        examples according to a provided rule.
        """
        if len(self.command_tokens) < 3:
            self.print_wrapper.error_log("Missing some arguments\nUsage: " +
                                         'rule "<rule>" [<number-of-examples]')
            return

        unit_type = CommandStrategy.get_unit_type_from_str(self.command_tokens[1])
        unit_name = CommandStrategy.remove_quotes(self.command_tokens[2])

        if unit_type == UnitType.alias:
            declaration = AliasDefinition(unit_name, None)
            relevant_dict = facade.parser.alias_definitions
        elif unit_type == UnitType.slot:
            declaration = SlotDefinition(unit_name, None)
            relevant_dict = facade.parser.slot_definitions
        else:  # intent
            declaration = IntentDefinition(unit_name, None)
            relevant_dict = facade.parser.intent_definitions

        if unit_name in relevant_dict:
            self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                     unit_name + "' is already defined.")
            return
        relevant_dict[unit_name] = declaration
        self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                 unit_name + "' was successfully declared.")
