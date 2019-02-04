"""
Module `chatette.cli.interactive_commnads.add_rule_command`.
Contains the strategy class that represents the interactive mode command
`add-rule` which allows to add a rule to a unit definition.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy


class AddRuleCommand(CommandStrategy):
    usage_str = 'add-rule <unit-type> "<unit-name>" "<rule>"'
    def __init__(self, command_str):
        super(AddRuleCommand, self).__init__(command_str)
    
    def execute(self, facade):
        

    def execute_on_unit(self, facade, unit_type, unit_name):
        #TODO
