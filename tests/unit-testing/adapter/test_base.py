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

    def test_generate_batch(self):
        for batch in Adapter._Adapter__generate_batch(["ex"], [], None):
            assert batch.index == 0
            assert len(batch.examples) == 1
            assert batch.examples[0] == "ex"
            assert len(batch.synonyms) == 0

        for batch in Adapter._Adapter__generate_batch(["a", "b"], [], 1):
            assert batch.index in (0, 1)
            assert len(batch.examples) == 1
            assert batch.examples[0] in ("a", "b")
            assert len(batch.synonyms) == 0
