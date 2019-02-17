"""
Test module.
Tests the functionalities in module
`chatette.cli.interactive_commands.rename_command`.
"""

import pytest

from test_command_strategy import new_facade, get_facade

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.cli.interactive_commands.rename_command import RenameCommand
from chatette.parsing.parser_utils import UnitType


def test_obj():
    cmd = RenameCommand("")
    assert cmd.command_tokens == []
    assert isinstance(cmd, CommandStrategy)

    cmd = RenameCommand('rename ~ "old" "new"')
    assert cmd.command_tokens == ["rename", "~", '"old"', '"new"']
    assert isinstance(cmd, CommandStrategy)


def test_err(capsys):
    facade = get_facade()
    cmd = RenameCommand('rename NOTHING "a" "b"')
    assert cmd.command_tokens == ["rename", "NOTHING", '"a"', '"b"']
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "[ERROR]\tUnknown unit type: 'NOTHING'." in captured.out

    cmd = RenameCommand("a")
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "[ERROR]\tMissing some arguments\n\tUsage: " + \
           'rename <unit-type> "<old-name>" "<new-name>"' in captured.out

    cmd = RenameCommand('rename alias "a" "b"')
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "[ERROR]\tCouldn't find a unit named 'a'." in captured.out


def test_execute():
    cmd = RenameCommand('rename alias "can you" "could you"')
    assert cmd.command_tokens == ["rename", "alias", '"can you"', '"could you"']
    facade = new_facade()
    cmd.execute(facade)
    with pytest.raises(KeyError):
        facade.parser.get_definition("can you", UnitType.alias)
    try:
        facade.parser.get_definition("could you", UnitType.alias)
    except KeyError:
        pytest.fail("Unexpected KeyError exception. Renaming didn't properly work.")

    cmd = RenameCommand('rename ~ "tell me" "a"')
    assert cmd.command_tokens == ["rename", "~", '"tell me"', '"a"']
    facade = new_facade()
    cmd.execute(facade)
    with pytest.raises(KeyError):
        facade.parser.get_definition("tell me", UnitType.alias)
    try:
        facade.parser.get_definition("a", UnitType.alias)
    except KeyError:
        pytest.fail("Unexpected KeyError exception. Renaming didn't properly work.")


def test_abstract_methods():
    cmd = RenameCommand('rename alias "a" "b"')
    with pytest.raises(NotImplementedError):
        cmd.execute_on_unit(None, None, None)
    with pytest.raises(NotImplementedError):
        cmd.finish_execution(None)
