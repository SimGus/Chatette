# codin: utf-8
"""
Test module.
Tests the functions in module `chatette.log`.
"""

from chatette import log


class TestPrints(object):
    def test_existences(self):
        assert "print_DBG" in dir(log)
        assert "print_warn" in dir(log)

    def test_no_return(self):
        assert log.print_DBG("Test") is None
        assert log.print_warn("Test") is None
