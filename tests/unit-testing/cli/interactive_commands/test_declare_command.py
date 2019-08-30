"""
Test module.
Tests the functionalities present in module
`chatette.cli.interactive_commands.decalre_command`.
"""

import pytest

from test_command_strategy import new_facade

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.cli.interactive_commands.declare_command import DeclareCommand

from chatette.utils import UnitType
from chatette.refactor_units.ast import AST


def test_obj():
    cmd = DeclareCommand("")
    assert cmd.command_tokens == []
    assert isinstance(cmd, CommandStrategy)

    cmd = DeclareCommand("declare alias /a/")
    assert cmd.command_tokens == ["declare", "alias", "/a/"]
    assert isinstance(cmd, CommandStrategy)


def test_err(capsys):
    facade = new_facade()

    cmd = DeclareCommand("declare")
    cmd.execute()
    captured = capsys.readouterr()
    assert "[ERROR]\tMissing some arguments\n\tUsage: " + \
           'declare <unit-type> "<unit-name>"' in captured.out

    cmd = DeclareCommand("declare nothing /a/")
    cmd.execute()
    captured = capsys.readouterr()
    assert "[ERROR]\tUnknown unit type: 'nothing'." in captured.out

    cmd = DeclareCommand('declare alias "var#a#b"')
    cmd.execute()
    captured = capsys.readouterr()
    assert "[ERROR]\tUnit identifier couldn't be interpreted. " + \
           "Did you mean to escape some hashtags '#'?" in captured.out

    cmd = DeclareCommand('declare alias "a#var"')
    cmd.execute()
    captured = capsys.readouterr()
    assert "[ERROR]\tVariation name detected, " + \
           "while units cannot be declared with a variation. " + \
           "Did you mean to escape some hashtags '#'?" in captured.out

    cmd = DeclareCommand('declare alias "var"')
    cmd.execute()
    captured = capsys.readouterr()
    assert "Alias 'var' is already defined."


def test_execute(capsys):
    print("AAAAAAAAAAAA")
    facade = new_facade()
    cmd = DeclareCommand('declare alias "machin"')
    cmd.execute()
    try:
        unit = AST.get_or_create()[UnitType.alias]["machin"]
        assert len(unit._variation_rules) == 0
        assert len(unit._all_rules) == 0
    except (KeyError, ValueError):
        pytest.fail("Unexpected error, 'declare' command didn't work.")
    
    captured = capsys.readouterr()
    assert "Alias 'machin' was successfully declared." in captured.out

    print("AAAAAAAAAAAA")
    facade = new_facade()
    cmd = DeclareCommand('declare slot "machin"')
    cmd.execute()
    try:
        unit = AST.get_or_create()[UnitType.slot]["machin"]
        assert len(unit._variation_rules) == 0
        assert len(unit._all_rules) == 0
    except (KeyError, ValueError):
        pytest.fail("Unexpected error, 'declare' command didn't work.")
    
    captured = capsys.readouterr()
    assert "Slot 'machin' was successfully declared." in captured.out

    print("AAAAAAAAAAAA")
    facade = new_facade()
    cmd = DeclareCommand('declare intent "machin"')
    cmd.execute()
    try:
        unit = AST.get_or_create()[UnitType.intent]["machin"]
        assert len(unit._variation_rules) == 0
        assert len(unit._all_rules) == 0
    except (KeyError, ValueError):
        pytest.fail("Unexpected error, 'declare' command didn't work.")
    
    captured = capsys.readouterr()
    assert "Intent 'machin' was successfully declared." in captured.out


def test_abstract_methods():
    cmd = DeclareCommand('declare alias "a"')
    with pytest.raises(NotImplementedError):
        cmd.execute_on_unit(None, None, None)
    with pytest.raises(NotImplementedError):
        cmd.finish_execution()
    
