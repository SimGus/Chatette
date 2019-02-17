"""
Module `chatette.cli.interactive_commands.rule_command`.
Contains the strategy class that represents the interactive mode command
`rule` which generates as many examples as asked that the provided rule
can generate.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.units.alias.definition import AliasDefinition
from chatette.units import ENTITY_MARKER


class RuleCommand(CommandStrategy):

    def execute(self, facade):
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
                self.print_wrapper.error_log("The number of examples asked (" +
                                             self.command_tokens[2] + ") is " +
                                             "a valid integer.")

        rule_tokens = facade.parser.tokenizer.tokenize(rule_str)
        rule = facade.parser.tokens_to_sub_rules(rule_tokens)
        definition = AliasDefinition("INTERNAL", None, [rule])
        try:
            examples = definition.generate_nb_examples(nb_examples)
            self.print_wrapper.write("Generated examples:")
            for ex in examples:
                self.print_wrapper.write(ex.text.replace(ENTITY_MARKER, ""))
        except KeyError as e:
            self.print_wrapper.error_log("Upon generation: " + str(e))


    # Override abstract methods
    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        raise NotImplementedError()
    def finish_execution(self, facade):
        raise NotImplementedError()
