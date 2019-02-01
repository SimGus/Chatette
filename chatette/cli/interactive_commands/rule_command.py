"""
Module `chatette.cli.interactive_commands.rule_command`.
Contains the strategy class that represents the interactive mode command
`rule` which generates as many examples as asked that the provided rule
can generate.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy


class RuleCommand(CommandStrategy):
    def __init__(self, command_str):
        super(RuleCommand, self).__init__(command_str)

    def execute(self, facade):
        """
        Implements the command `rule` which generates a certain number of
        examples according to a provided rule.
        """
        if len(self.command_tokens) < 2:
            self.print_wrapper.error_log("Missing some arguments\nUsage: " +
                                         'rule "<rule>" [<number-of-examples]')
            return
        
        rule = CommandStrategy.remove_quotes(self.command_tokens[1])
        nb_examples = None
        if len(self.command_tokens) >= 3:
            try:
                nb_examples = int(self.command_tokens[2])
            except ValueError:
                self.print_wrapper.error_log("The number of examples asked (" +
                                             self.command_tokens[2] + ") is " +
                                             "a valid integer.")
        # TODO
