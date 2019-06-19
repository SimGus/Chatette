"""
Test module.
Tests the functionalities present in module
`chatette.cli.interactive_commands.delete_command`.
"""

import pytest

from test_command_strategy import new_facade

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.cli.interactive_commands.delete_command import DeleteCommand
from chatette.parsing.parser_utils import UnitType


def test_obj():
    cmd = DeleteCommand("")
    assert cmd.command_tokens == []
    assert isinstance(cmd, CommandStrategy)


def test_execute(capsys):
    cmd = DeleteCommand('delete alias "inexistant"')
    cmd.execute(new_facade())
    captured = capsys.readouterr()
    assert "Alias 'inexistant' was not defined." in captured.out

    cmd = DeleteCommand('delete alias "tell me"')
    facade = new_facade()
    try:
        facade.parser.ast.get_definition("tell me", UnitType.alias)
    except KeyError:
        pytest.fail("Unexpected KeyError. Alias 'tell me' doesn't exist " + \
                    "in the parser.")
    cmd.execute(facade)
    with pytest.raises(KeyError):
        facade.parser.ast.get_definition("tell me", UnitType.alias)
    captured = capsys.readouterr()
    assert "Alias 'tell me' was successfully deleted." in captured.out
