"""
Module `chatette.cli.interactive_command.save_command`.
Contains the strategy class that represents the interactive mode command
`save` which writes a template file that, when parsed, would make a parser
that is in the state of the current parser.
"""

from __future__ import print_function
import io

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.utils import cast_to_unicode

from chatette.units.ast import AST


class SaveCommand(CommandStrategy):
    usage_str = 'save <template-file-path>'

    def execute(self):
        if len(self.command_tokens) < 2:
            self.print_wrapper.error_log("Missing some arguments\nUsage: " +
                                         self.usage_str)
            return

        template_filepath = self.command_tokens[1]
        definitions = AST.get_or_create()
        with io.open(template_filepath, 'w+') as f:
            for intent_name in definitions._intent_definitions:
                intent = definitions._intent_definitions[intent_name]
                print(cast_to_unicode(intent.as_template_str() + '\n'), file=f)
            print(cast_to_unicode(''), file=f)
            for alias_name in definitions._alias_definitions:
                alias = definitions._alias_definitions[alias_name]
                print(cast_to_unicode(alias.as_template_str() + '\n'), file=f)
            print(cast_to_unicode(''), file=f)
            for slot_name in definitions._slot_definitions:
                slot = definitions._slot_definitions[slot_name]
                print(cast_to_unicode(slot.as_template_str() + '\n'), file=f)
            print(cast_to_unicode(''), file=f)
        self.print_wrapper.write("Template file successfully written.")


    # Override abstract methods
    def execute_on_unit(self, unit_type, unit_name, variation_name=None):
        raise NotImplementedError()
    def finish_execution(self):
        raise NotImplementedError()
