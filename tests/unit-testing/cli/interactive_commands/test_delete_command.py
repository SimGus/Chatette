"""
Test module.
Tests the functionalities present in module
`chatette.cli.interactive_commands.delete_command`.
"""

import pytest

from test_command_strategy import new_facade

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.cli.interactive_commands.delete_command import DeleteCommand
from chatette.utils import UnitType

from chatette.units.ast import AST


def test_obj():
    cmd = DeleteCommand("")
    assert cmd.command_tokens == []
    assert isinstance(cmd, CommandStrategy)


def test_execute(capsys):
    new_facade()

    cmd = DeleteCommand('delete alias "inexistant"')
    cmd.execute()
    captured = capsys.readouterr()
    assert "Alias 'inexistant' was not defined." in captured.out

    cmd = DeleteCommand('delete alias "tell me"')
    new_facade()
    try:
        AST.get_or_create()[UnitType.alias]["tell me"]
    except KeyError:
        pytest.fail("Unexpected KeyError. Alias 'tell me' doesn't exist " + \
                    "in the parser.")
    cmd.execute()
    with pytest.raises(KeyError):
        AST.get_or_create()[UnitType.alias]["tell me"]
    captured = capsys.readouterr()
    assert "Alias 'tell me' was successfully deleted." in captured.out
