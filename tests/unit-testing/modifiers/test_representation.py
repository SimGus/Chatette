# coding: utf-8
"""
Test module.
Tests the functionalities that are present in module
`chatette.modifiers.representation`
"""


from chatette.modifiers.representation import ModifiersRepresentation


class TestModifiersRepr(object):
    def test_default(self):
        repr = ModifiersRepresentation()
        assert not repr.casegen
        assert repr.variation_name is None
        assert not repr.randgen
        assert repr.randgen_name is None
        assert repr.randgen_percent == 50
        assert repr.argument_name is None
        assert repr.argument_value is None

    def test_str(self):
        repr = ModifiersRepresentation()
        assert \
            str(repr) == \
                "ModifiersRepresentation(casegen: False randgen: None (50) " + \
                "arg name: None arg value: None)"
    
    def test_short_desc(self):
        repr = ModifiersRepresentation()
        assert repr.short_description() == "No modifiers\n"

        repr.casegen = True
        assert repr.short_description() == "Modifiers:\n- case generation\n"

        repr.casegen = False
        repr.randgen = True
        repr.randgen_name = "test"
        assert \
            repr.short_description() == \
                "Modifiers:\n- random generation: test (50%)\n"
        
        repr.randgen = False
        repr.argument_name = "test"
        assert \
            repr.short_description() == "Modifiers:\n- argument name: test\n"
        
        repr.argument_name = None
        repr.argument_value = "test"
        assert \
            repr.short_description() == "Modifiers:\n- argument value: test\n"
