# coding: utf-8
"""
Test module.
Tests the functionalities present in module
`chatette.adapters.rasa`.
"""

from chatette.adapters.rasa import RasaAdapter


class TestRasaAdapter(object):
    def test_constructor(self):
        adapter = RasaAdapter()
        assert adapter._batch_size == 10000
        assert adapter._base_filepath is None

        adapter = RasaAdapter("path", 10)
        assert adapter._batch_size == 10
        assert adapter._base_filepath == "path"
    
    def test_get_file_extension(self):
        assert RasaAdapter._get_file_extension() == "json"

    def test_format_synonyms(self):
        synonyms = {
            u'Edinburgh': [u'Edinburgh'],
            u'Paris': [u'Paris'], u'Berlin': [u'Berlin'],
            u'London': [u'London'], u'Amsterdam': [u'Amsterdam'],
            u'Brussels': [u'Brussels'], u'tomorrow': [u'tomorrow'],
            u'today': [u'now', u'today']
        }
        formatted_synonyms = \
            RasaAdapter._RasaAdapter__format_synonyms(synonyms)
        assert \
            formatted_synonyms == [
                {"value": u'today', "synonyms": [u'now', u'today']}
            ]
