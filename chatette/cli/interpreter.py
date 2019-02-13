"""
Module `chatette.cli`
Contains the interpreter that runs in a terminal in interactive mode.
"""

from __future__ import print_function
import io

from chatette import __version__
from chatette.utils import print_DBG

from chatette.cli.interactive_commands import exit_command, stats_command, \
                                              parse_command, exist_command, \
                                              rename_command, delete_command, \
                                              examples_command, hide_command, \
                                              unhide_command, execute_command, \
                                              show_command, rule_command, \
                                              generate_command, \
                                              add_rule_command, declare_command, \
                                              set_modifier_command, save_command


class CommandLineInterpreter(object):
    def __init__(self, facade, commands_file_path):
        self.facade = facade
        self._dont_enter_interactive_mode = True
        self.introduce()
        if commands_file_path is not None:
            self._dont_enter_interactive_mode = \
                self._execute_commands_file(commands_file_path)
        else:
            self._dont_enter_interactive_mode = False


    def _execute_commands_file(self, commands_file_path):
        """
        Opens the file at `commands_file_path` and
        execute all the commands that are inside it, one command per line
        (except lines starting with `//`). Stops the execution if a line is not
        a valid command.
        Returns `True` if the interactive mode shouldn't be entered and 
        `False` otherwise.
        """
        print("Executing commands from file " + commands_file_path)
        stop = False
        with io.open(commands_file_path, 'r') as f:
            for l in f:
                if not l.isspace() and not l.lstrip().startswith("//"):
                    stop = self.interpret_command(l.rstrip(), quiet=True)
                    if stop:
                        break
        print("Execution of file over.")
        return stop


    def introduce(self):
        """
        Tells the user they are in interactive mode and
        asks the facade to execute the parsing of the master file if needed.
        """
        print("Chatette v"+__version__+" running in *interactive mode*.")
        self.facade.run_parsing()

    def wait_for_input(self):
        """
        Waits for the user to type a command, interprets it and executes it.
        """
        if self._dont_enter_interactive_mode:
            return
        stop = False
        while True:
            print(">>> ", end='')
            try:
                command_str = input()
            except EOFError:
                print("Exiting interactive mode")
                break
            stop = self.interpret_command(command_str)
            if stop:
                print("Exiting interactive mode")
                break

    def interpret_command(self, command_str, quiet=False):
        """
        Interprets the command `command_str` and executes it.
        Returns `True` if the interactive mode should be exited.
        """
        if command_str == "" or command_str.isspace():
            return False
        command = CommandLineInterpreter.get_command(command_str, quiet)
        if command is None:
            return False
        if command.should_exit():
            return True
        result = command.execute(self.facade)
        if isinstance(command, execute_command.ExecuteCommand):
            self.execute_commands(result)
        command.flush_output()
        return False

    def execute_commands(self, commands):
        """
        Executes the list of commands `commands`
        as if they had been typed in by the user.
        Returns `True` if the interactive mode should be exited.
        """
        if commands is None:
            return False
        for cmd in commands:
            stop = self.interpret_command(cmd)
            if stop:
                return True
        return False


    @staticmethod
    def get_command(command_str, quiet):
        """Factory method: creates the right command from the provided str."""
        operation_name = command_str.split(maxsplit=1)[0].lower()
        if operation_name == "exit":
            return exit_command.ExitCommand(command_str, quiet)
        if operation_name == "stats":
            return stats_command.StatsCommand(command_str, quiet)
        if operation_name == "parse":
            return parse_command.ParseCommand(command_str, quiet)
        if operation_name == "exist":
            return exist_command.ExistCommand(command_str, quiet)
        if operation_name == "rename":
            return rename_command.RenameCommand(command_str, quiet)
        if operation_name == "delete":
            return delete_command.DeleteCommand(command_str, quiet)
        if operation_name == "examples":
            return examples_command.ExamplesCommand(command_str, quiet)
        if operation_name == "hide":
            return hide_command.HideCommand(command_str, quiet)
        if operation_name == "unhide":
            return unhide_command.UnhideCommand(command_str, quiet)
        if operation_name == "execute":
            return execute_command.ExecuteCommand(command_str, quiet)
        if operation_name == "show":
            return show_command.ShowCommand(command_str, quiet)
        if operation_name == "rule":
            return rule_command.RuleCommand(command_str, quiet)
        if operation_name == "generate":
            return generate_command.GenerateCommand(command_str, quiet)
        if operation_name == "add-rule":
            return add_rule_command.AddRuleCommand(command_str, quiet)
        if operation_name == "declare":
            return declare_command.DeclareCommand(command_str, quiet)
        if operation_name == "set-modifier":
            return set_modifier_command.SetModifierCommand(command_str, quiet)
        if operation_name == "save":
            return save_command.SaveCommand(command_str, quiet)
        if not quiet:
            print("Unknown command: " + operation_name)
        return None
