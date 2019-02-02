"""
Module `chatette.cli.interactive_commands.show_command`.
Contains the strategy class that represents the interactive mode command
`show` which shows information about a unit definition and lists a bunch of
its rules (all if possible).
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy


class ShowCommand(CommandStrategy):
    max_nb_rules_to_display = 12
    def __init__(self, command_str):
        super(ShowCommand, self).__init__(command_str)
    
    def execute(self, facade):
        """
        Implements the command `show` which shows information about a specific
        unit definition and lists its rules (or just several of them if there
        are too many rules).
        """
        # TODO support variations
        if len(self.command_tokens) < 3:
            self.print_wrapper.error_log("Missing some arguments\nUsage: " +
                                         'show <unit-type> "<unit-name>"')
            return
        
        unit_type = CommandStrategy.get_unit_type_from_str(self.command_tokens[1])
        unit_name = CommandStrategy.remove_quotes(self.command_tokens[2])
        try:
            unit = facade.parser.get_definition(unit_name, unit_type)
            self.print_wrapper.write(unit.short_desc_str())
            self.print_wrapper.write("Rules:")
            rules = unit.rules
            for (i, rule) in enumerate(rules):
                if i >= self.max_nb_rules_to_display:
                    break
                rule_str = ''.join([sub_rule.as_string() for sub_rule in rule])
                self.print_wrapper.write('\t'+rule_str)
        except KeyError:
            self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                     unit_name + "' is not defined.")

