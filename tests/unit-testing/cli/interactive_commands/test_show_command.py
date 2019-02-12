"""
Test module
Tests the functionalities contained in module
`chatette.cli.interactive_commands.show_command`.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.cli.interactive_commands.show_command import ShowCommand

from test_command_strategy import get_facade


def test_obj():
    cmd = ShowCommand("")
    assert isinstance(cmd, CommandStrategy)
    assert cmd.command_tokens == []

    cmd = ShowCommand("show ~ /a/")
    assert isinstance(cmd, CommandStrategy)
    assert cmd.command_tokens == ["show", "~", "/a/"]


def test_execute(capsys):
    cmd = ShowCommand('show alias "sorry"')
    assert cmd.command_tokens == ["show", "alias", '"sorry"']
    facade = get_facade()
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "alias: 'sorry'\nmodifiers:\n\tNone\nVariations: 0" in captured.out

    # cmd = ShowCommand('show ~ /o/g')
    # assert cmd.command_tokens ==  ["show", "~", "/o/g"]
    # cmd.execute(facade)
    # captured = capsys.readouterr()
    # assert "alias: 'can you'\nmodifiers:\n\tNone\nVariations: 0" in captured.out
    # assert "alias: 'sorry'\nmodifiers:\n\tNone\nVariations: 0" in captured.out
