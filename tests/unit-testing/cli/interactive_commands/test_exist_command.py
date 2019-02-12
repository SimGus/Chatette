"""
Test module
Tests the functionalities present in module
`chatette.cli.interactive_commands.exist_command`.
"""

from chatette.parsing.parser import Parser
from chatette.facade import Facade
from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.cli.interactive_commands.exist_command import ExistCommand


def test_obj():
    cmd = ExistCommand("")
    assert isinstance(cmd, CommandStrategy)
    assert cmd.command_tokens == []

    cmd = ExistCommand("exist ~ /a/")
    assert isinstance(cmd, CommandStrategy)
    assert cmd.command_tokens == ["exist", "~", "/a/"]


FACADE = None
def get_facade():
    global FACADE
    if FACADE is None:
        FACADE = \
            Facade("tests/unit-testing/cli/interactive_commands/toilets.chatette",
                   "tests/unit-testing/cli/interactive_commands/", None, False,
                   None)
    return FACADE

def test_execute(capsys):
    cmd = ExistCommand('exist alias "sorry"')
    assert cmd.command_tokens == ["exist", "alias", '"sorry"']
    facade = get_facade()
    facade.run_parsing()
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "alias: 'sorry'\nmodifiers:\n\tNone\nVariations: 0" in captured.out

    cmd = ExistCommand('exist ~ /o/g')
    assert cmd.command_tokens ==  ["exist", "~", "/o/g"]
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "alias: 'can you'\nmodifiers:\n\tNone\nVariations: 0\n\n" + \
           "alias: 'sorry'\nmodifiers:\n\tNone\nVariations: 0" in captured.out
