"""
Module `chatette.cli.interactive_commands.set_modifier_command`.
Contains the strategy class that represents the interactive mode command
`set-modifier` which allows to change the value of the modifier of a unit
declaration.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.utils import str_to_bool
from chatette.parsing.parser_utils import CASE_GEN_SYM, ARG_SYM


class SetModifierCommand(CommandStrategy):
    usage_str = 'set-modifier <unit-type> "<unit-type>" ' + \
                '<modifer-name> "<value>"'

    def execute(self, facade):
        if len(self.command_tokens) < 5:
            self.print_wrapper.error_log("Missing some arguments\nUsage: " +
                                         self.usage_str)
            return

        unit_type = CommandStrategy.get_unit_type_from_str(self.command_tokens[1])
        unit_regex = self.get_regex_name(self.command_tokens[2])

        modifier_name = self.command_tokens[3]
        modifier_value = CommandStrategy.remove_quotes(self.command_tokens[4])

        if unit_regex is None:
            unit_name = CommandStrategy.remove_quotes(self.command_tokens[2])
            self._set_modifier(facade.parser, unit_type, unit_name,
                               modifier_name, modifier_value)
        else:
            count = 0
            for unit_name in self.next_matching_unit_name(facade.parser,
                                                          unit_type,
                                                          unit_regex):
                self._set_modifier(facade.parser, unit_type, unit_name,
                                   modifier_name, modifier_value)
                count += 1
            if count == 0:
                self.print_wrapper.write("No " + unit_type.name + " matched.")

    def _set_modifier(self, parser, unit_type, unit_name, modifier_name, value):
        unit = parser.get_definition(unit_name, unit_type)
        modifier_name = modifier_name.lower()
        if modifier_name in ("casegen", CASE_GEN_SYM):
            try:
                value = str_to_bool(value)
                unit.casegen = value
            except ValueError:
                self.print_wrapper.write("Invalid value for case generation " +
                                         "modifier (True or False).")
                return
        elif modifier_name in ("arg", ARG_SYM):
            unit.set_arg(value)
        else:
            self.print_wrapper.write("Invalid modifier selected (can be "+
                                     "'casegen' or 'arg').")
            return
        self.print_wrapper.write("Modifier for " + unit_type.name + " '" +
                                 unit_name + "' successfully changed.")

