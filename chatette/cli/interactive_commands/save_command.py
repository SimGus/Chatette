"""
Module `chatette.cli.interactive_command.save_command`.
Contains the strategy class that represents the interactive mode command
`save` which writes a template file that, when parsed, would make a parser
that is in the state of the current parser.
"""

from __future__ import print_function
import io

from chatette.cli.interactive_commands.command_strategy import CommandStrategy


class SaveCommand(CommandStrategy):
    usage_str = 'save <template-file-path>'

    def execute(self, facade):
        if len(self.command_tokens) < 2:
            self.print_wrapper.error_log("Missing some arguments\nUsage: " +
                                         self.usage_str)
            return

        template_filepath = self.command_tokens[1]
        definitions = facade.parser.ast
        with io.open(template_filepath, 'w+') as f:
            for intent_name in definitions.intent_definitions:
                intent = definitions.intent_definitions[intent_name]
                print(intent.get_template_description(), file=f)
            print(file=f)
            for alias_name in definitions.alias_definitions:
                alias = definitions.alias_definitions[alias_name]
                print(alias.get_template_description(), file=f)
            print(file=f)
            for slot_name in definitions.slot_definitions:
                slot = definitions.slot_definitions[slot_name]
                print(slot.get_template_description(), file=f)
        self.print_wrapper.write("Template file successfully written.")


    # Override abstract methods
    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        raise NotImplementedError()
    def finish_execution(self, facade):
        raise NotImplementedError()
