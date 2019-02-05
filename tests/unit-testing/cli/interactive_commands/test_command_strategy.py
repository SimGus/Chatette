"""
Test module.
Tests the functions
in module `chatette.cli.interactive_commands.command_strategy`.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.cli.terminal_writer import RedirectionType
from chatette.parsing.parser_utils import UnitType


class TestSTokenize(object):
    def test_empty(self):
        assert CommandStrategy.tokenize("") == []
    
    def test_short_commands(self):
        assert CommandStrategy.tokenize("exit") == ["exit"]
        assert CommandStrategy.tokenize("stats  ") == ["stats"]
        assert CommandStrategy.tokenize("NOT-command") == ["NOT-command"]
        assert CommandStrategy.tokenize("NOT COMMAND") == ["NOT", "COMMAND"]
        assert CommandStrategy.tokenize('word "a name"') == ["word", '"a name"']
        assert CommandStrategy.tokenize(' open "quote a') == ["open", '"quote a']

    def test_long_commands(self):
        assert CommandStrategy.tokenize('rule "~[a rule] tested"') == \
               ["rule", '"~[a rule] tested"']
        assert CommandStrategy.tokenize('set-modifier alias "something else" ' +
                                        'casegen "True"\t') == \
               ["set-modifier", "alias", '"something else"', "casegen", '"True"']
    
    def test_escapement(self):
        assert CommandStrategy.tokenize('test "escaped \\" was here"') == \
               ["test", '"escaped \\" was here"']


class TestFindRedirectionFilePath(object):
    @staticmethod
    def to_tokens(text):
        return CommandStrategy.tokenize(text)

    def test_empty(self):
        assert CommandStrategy.find_redirection_file_path(self.to_tokens("")) is None
    
    def test_no_redirection(self):
        assert CommandStrategy.find_redirection_file_path(self.to_tokens("exit")) is None
        assert CommandStrategy.find_redirection_file_path(self.to_tokens("test something")) is None
        assert CommandStrategy.find_redirection_file_path(self.to_tokens(
                    'long command "with quotes\" inside"'
               )) is None
    
    def test_truncate_redirection(self):
        assert CommandStrategy.find_redirection_file_path(self.to_tokens("stats > test.txt")) == \
               (RedirectionType.truncate, "test.txt")
        assert CommandStrategy.find_redirection_file_path(self.to_tokens(
                    "another rule > different/path.extension"
               )) == (RedirectionType.truncate, "different/path.extension")
        assert CommandStrategy.find_redirection_file_path(self.to_tokens(
                    'rule "with quotes\" and escapements" > /path/no/extension'
               )) == (RedirectionType.truncate, "/path/no/extension")
    
    def test_append_redirection(self):
        assert CommandStrategy.find_redirection_file_path(self.to_tokens("stats >> file.cc")) == \
               (RedirectionType.append, "file.cc")
        assert CommandStrategy.find_redirection_file_path(self.to_tokens(
                    "a command >> small/path.ext"
               )) == (RedirectionType.append, "small/path.ext")
    
    def test_quiet(self):
        assert CommandStrategy.find_redirection_file_path(self.to_tokens("stats >>")) == \
               (RedirectionType.quiet, None)
        assert CommandStrategy.find_redirection_file_path(self.to_tokens("exit >")) == \
               (RedirectionType.quiet, None)
        assert CommandStrategy.find_redirection_file_path(self.to_tokens("command >  ")) == \
               (RedirectionType.quiet, None)


class TestGetUnitTypeFromStr(object):
    def test_wrong_str(self):
        assert CommandStrategy.get_unit_type_from_str("") is None
        assert CommandStrategy.get_unit_type_from_str("t") is None
        assert CommandStrategy.get_unit_type_from_str("test") is None
        assert CommandStrategy.get_unit_type_from_str("SOMETHING") is None
        assert CommandStrategy.get_unit_type_from_str("\t\t ") is None
    
    def test_correct_str(self):
        assert CommandStrategy.get_unit_type_from_str("alias") == UnitType.alias
        assert CommandStrategy.get_unit_type_from_str("AliaS") == UnitType.alias
        assert CommandStrategy.get_unit_type_from_str("slot") == UnitType.slot
        assert CommandStrategy.get_unit_type_from_str("SLOT") == UnitType.slot
        assert CommandStrategy.get_unit_type_from_str("intent") == UnitType.intent
        assert CommandStrategy.get_unit_type_from_str("iNtENt") == UnitType.intent
