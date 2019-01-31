"""
Module `chatette.cli.interactive_commands.command_strategy`.
Contains the base class for all the commands that can be used with
the interactive mode, such that such a command will subclass this base class
in order to implement the strategy design pattern.
"""

from chatette.parsing.parser_utils import UnitType
from chatette.cli.terminal_writer import TerminalWriter, RedirectionType


REDIRECTION_SYM = ">"
REDIRECTION_APPEND_SYM = ">>"


class CommandStrategy(object):
    def __init__(self, command_str):
        self.command_tokens = CommandStrategy.tokenize(command_str)
        redirection_tuple = \
                CommandStrategy.find_redirection_file_path(self.command_tokens)
        print("tup", redirection_tuple)
        if redirection_tuple is None:
            self.print_wrapper = TerminalWriter(None)
        else:
            (redirection_type, redirection_filepath) = redirection_tuple
            self.print_wrapper = TerminalWriter(redirection_type,
                                                redirection_filepath)

    @staticmethod
    def tokenize(command_str):
        """Tokenizes a string that is a command."""
        splitted = command_str.split()
        if len(splitted) == 0:
            return []
        if len(splitted) == 1:
            return [splitted[0]]
        tokens = []
        current_token = ""
        inside_token = False
        for word in splitted:
            if inside_token:
                current_token += word + ' '
                if word.endswith('"'):
                    inside_token = False
                    tokens.append(current_token.rstrip())
                    current_token = ""
            elif word.startswith('"') and word.endswith('"'):
                tokens.append(word)
            elif word.startswith('"'):
                inside_token = True
                current_token += word + ' '
            else:  # not inside a token and not starting with "
                tokens.append(word)
        if current_token != "":
            tokens.append(current_token.rstrip())
        return tokens
    
    @staticmethod
    def find_redirection_file_path(tokens):
        """
        Finds the path of the file
        which the output of a command should be redirected to and
        returns it along with the type of redirection that it is (in a 2-tuple).
        The type of redirection is an enumeration item of type
        `RedirectionType`.
        Returns `None` if no redirection was found.
        """
        if len(tokens) < 3:
            return None
        if tokens[-2] == REDIRECTION_APPEND_SYM:
            return (RedirectionType.append, tokens[-1])
        if tokens[-2] == REDIRECTION_SYM:
            return (RedirectionType.truncate, tokens[-1])
        return None

    @staticmethod
    def get_unit_type_from_str(unit_type_str):
        """
        Transforms the string `unit_type_str`
        into the corresponding `UnitType` value.
        Returns `None` if there exist no corresponding `UnitType` value.
        """
        unit_type_str = unit_type_str.lower()
        if unit_type_str == "alias":
            return UnitType.alias
        if unit_type_str == "slot":
            return UnitType.slot
        if unit_type_str == "intent":
            return UnitType.intent
        return None

    @staticmethod
    def remove_quotes(text):
        """
        Remove the double quotes at the beginning and end of `text` and
        remove the escapement of other quotes.
        """
        return text[1:-1].replace(r'\"', '"')


    def flush_output(self):
        """
        Asks the wrapper of print to flush its outputs
        to the redirected file (if such a file exists).
        """
        self.print_wrapper.flush()


    def should_exit(self):
        """Returns `True` if the program should exit the interactive mode."""
        return False

    def execute(self, facade):
        """
        Executes the command represented by this object.
        `facade` is a facade to the whole system (contains links to the parser).
        This method should be overriden by subclasses.
        """
        raise NotImplementedError()
