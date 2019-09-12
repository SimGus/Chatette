"""
Test module.
Tests the functions in module 'chatette.utils'.
"""


from chatette.deprecations import Deprecations


class TestDeprecations(object):
    def test_new(self):
        instance = Deprecations()
        same = Deprecations.get_or_create()
        assert instance == same
        assert not instance._old_comment_warned
        assert not instance._old_choice_warned
    
    def test_warn_old_comment(self, capsys):
        instance = Deprecations.reset_instance()
        assert not instance._old_comment_warned
        assert not instance._old_choice_warned

        instance.warn_old_comment()
        assert instance._old_comment_warned
        assert not instance._old_choice_warned

        captured = capsys.readouterr()
        assert "Comments starting with a semi-colon" in captured.err

    def test_warn_old_choice(self, capsys):
        instance = Deprecations.reset_instance()
        assert not instance._old_comment_warned
        assert not instance._old_choice_warned

        instance.warn_old_choice()
        assert not instance._old_comment_warned
        assert instance._old_choice_warned

        captured = capsys.readouterr()
        assert "Choices starting with " in captured.err
