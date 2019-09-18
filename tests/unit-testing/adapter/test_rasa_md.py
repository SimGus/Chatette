# coding: utf-8
"""
Test module.
Tests the functionalities present in module
`chatette.adapters.rasa_md`.
"""

from chatette.adapters.rasa_md import RasaMdAdapter


class TestRasaMdAdapter(object):
    def test_constructor(self):
        adapter = RasaMdAdapter()
        assert adapter._batch_size is None
        assert adapter._base_filepath is None

        adapter = RasaMdAdapter("path")
        assert adapter._batch_size is None
        assert adapter._base_filepath == "path"
    
    def test_get_file_extension(self):
        assert RasaMdAdapter._get_file_extension() == "md"

    def test_format_synonyms(self):
        synonyms = {
            u'Edinburgh': [u'Edinburgh'],
            u'Paris': [u'Paris'], u'Berlin': [u'Berlin'],
            u'London': [u'London'], u'Amsterdam': [u'Amsterdam'],
            u'Brussels': [u'Brussels'], u'tomorrow': [u'tomorrow'],
            u'today': [u'now', u'today']
        }
        formatted_synonyms = \
            RasaMdAdapter._RasaMdAdapter__format_synonyms(synonyms)
        assert formatted_synonyms == "## synonym:today\n- now\n\n"
