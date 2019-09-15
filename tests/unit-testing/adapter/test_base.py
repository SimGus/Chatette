# coding: utf-8
"""
Test module.
Tests the functionalities that are present in module
`chatette.adapters._base`
"""

import pytest

from chatette.adapters._base import Batch, Adapter


class TestBatch(object):
    def test_constructor(self):
        batch = Batch(2, [], [])
        assert batch.index == 2
        assert len(batch.examples) == 0
        assert len(batch.synonyms) == 0


class TestAdapter(object):
    def test_abstract(self):
        with pytest.raises(TypeError):
            adapter = Adapter()
