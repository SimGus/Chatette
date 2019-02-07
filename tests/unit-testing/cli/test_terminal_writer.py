"""
Test module.
Tests the functions and methods in module `chatette.cli.terminal_writer`.
"""

from chatette.cli.terminal_writer import RedirectionType, TerminalWriter


class TestInitTerminalWriter(object):
    def test(self):
        obj = TerminalWriter()
        assert obj.redirection_file_path is None
        assert obj.buffered_text is None
        assert obj.file_mode == 'a+'

        obj = TerminalWriter(RedirectionType.append)
        assert obj.redirection_file_path is None
        assert obj.buffered_text is None
        assert obj.file_mode == 'a+'

        obj = TerminalWriter(RedirectionType.truncate)
        assert obj.redirection_file_path is None
        assert obj.buffered_text is None
        assert obj.file_mode == 'w+'

        obj = TerminalWriter(RedirectionType.quiet)
        assert obj.redirection_file_path is None
        assert obj.buffered_text is None
        assert obj.file_mode == 'quiet'

        obj = TerminalWriter(None)
        assert obj.redirection_file_path is None
        assert obj.buffered_text is None
        assert obj.file_mode is None

        obj = TerminalWriter(redirection_file_path="test")
        assert obj.redirection_file_path == "test"
        assert obj.buffered_text is None
        assert obj.file_mode == 'a+'


class TestReset(object):
    def test(self):
        obj = TerminalWriter(redirection_file_path="test")
        obj.reset()
        assert obj.redirection_file_path is None
        assert obj.buffered_text is None


class TestGetRedirection(object):
    def test(self):
        obj = TerminalWriter()
        assert obj.get_redirection() == (RedirectionType.append, None)

        obj = TerminalWriter(RedirectionType.append)
        assert obj.get_redirection() == (RedirectionType.append, None)

        obj = TerminalWriter(RedirectionType.truncate)
        assert obj.get_redirection() == (RedirectionType.truncate, None)

        obj = TerminalWriter(RedirectionType.quiet)
        assert obj.get_redirection() == (RedirectionType.quiet, None)

        obj = TerminalWriter(None)
        assert obj.get_redirection() is None

        obj = TerminalWriter(redirection_file_path="test")
        assert obj.get_redirection() == (RedirectionType.append, "test")


class TestWrite(object):
    def test_print(self, capsys):
        obj = TerminalWriter(None)
        obj.write("this is a test")
        captured = capsys.readouterr()
        assert captured.out == "this is a test\n"
        assert obj.buffered_text is None

    def test_quiet(self):
        obj = TerminalWriter(RedirectionType.quiet)
        obj.write("something")
        assert obj.buffered_text is None
    
    def test_not_quiet(self):
        obj = TerminalWriter(RedirectionType.append)
        obj.write("something")
        assert obj.buffered_text == "something"
        obj.write("other line")
        assert obj.buffered_text == "something\nother line"


class TestErrorLog(object):
    def test_print(self, capsys):
        obj = TerminalWriter(None)
        obj.error_log("this is a test")
        captured = capsys.readouterr()
        assert captured.out == "[ERROR]\tthis is a test\n"
        assert obj.buffered_text is None

    def test_quiet(self):
        obj = TerminalWriter(RedirectionType.quiet)
        obj.error_log("something")
        assert obj.buffered_text is None
    
    def test_not_quiet(self):
        obj = TerminalWriter(RedirectionType.append)
        obj.error_log("something")
        assert obj.buffered_text == "[ERROR]\tsomething"
        obj.error_log("other line")
        assert obj.buffered_text == "[ERROR]\tsomething\n[ERROR]\tother line"


class TestFlush(object):
    pass  # TODO
