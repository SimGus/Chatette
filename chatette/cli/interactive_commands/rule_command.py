"""
Module `chatette.cli.interactive_commands.rule_command`.
Contains the strategy class that represents the interactive mode command
`rule` which generates as many examples as asked that the provided rule
can generate.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy

from chatette.parsing.parser import Parser


class RuleCommand(CommandStrategy):
    def execute(self):
        """
        Implements the command `rule` which generates a certain number of
        examples according to a provided rule.
        """
        if len(self.command_tokens) < 2:
            self.print_wrapper.error_log("Missing some arguments\nUsage: " +
                                         'rule "<rule>" [<number-of-examples]')
            return

        rule_str = CommandStrategy.remove_quotes(self.command_tokens[1])
        nb_examples = None
        if len(self.command_tokens) >= 3:
            try:
                nb_examples = int(self.command_tokens[2])
            except ValueError:
                self.print_wrapper.error_log(
                    "The number of examples asked (" + \
                    self.command_tokens[2] + ") is a valid integer."
                )

        parser = Parser(None)
        rule_tokens = parser.lexer.lex("\t" + rule_str)
        # pylint: disable=protected-access
        rule = parser._parse_rule(rule_tokens[1:])

        if nb_examples is None:
            examples = rule.generate_all()
        else:
            examples = rule.generate_nb_possibilities(nb_examples)
        self.print_wrapper.write("Generated examples:")
        for ex in examples:
            self.print_wrapper.write(str(ex))


    # Override abstract methods
    def execute_on_unit(self, unit_type, unit_name, variation_name=None):
        raise NotImplementedError()
    def finish_execution(self):
        raise NotImplementedError()
