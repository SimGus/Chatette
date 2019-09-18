# coding: utf-8
"""
Test module.
Tests the functionalities present in module
`chatette.adapters.jsonl`.
"""

from chatette.adapters.jsonl import JsonListAdapter


class TestJsonListAdapter(object):
    def test_constructor(self):
        adapter = JsonListAdapter()
        assert adapter._batch_size == 10000
        assert adapter._base_filepath is None

        adapter = JsonListAdapter("path", 10)
        assert adapter._batch_size == 10
        assert adapter._base_filepath == "path"
    
    def test_file_extension(self):
        assert JsonListAdapter._get_file_extension() == "jsonl"
    
    def test_synonym_format(self):
        synonyms = {
            u'Edinburgh': [u'Edinburgh'],
            u'Paris': [u'Paris'], u'Berlin': [u'Berlin'],
            u'London': [u'London'], u'Amsterdam': [u'Amsterdam'],
            u'Brussels': [u'Brussels'], u'tomorrow': [u'tomorrow'],
            u'today': [u'now', u'today']
        }
        formatted_synonyms = \
            JsonListAdapter._JsonListAdapter__format_synonyms(synonyms)
        assert formatted_synonyms == {u'today': [u'now', u'today']}
        