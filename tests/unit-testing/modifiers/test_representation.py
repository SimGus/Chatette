# coding: utf-8
"""
Test module.
Tests the functionalities that are present in module
`chatette.modifiers.representation`
"""


from chatette.modifiers.representation import \
    ModifiersRepresentation, RandgenRepresentation


class TestModifiersRepr(object):
    def test_default(self):
        repr = ModifiersRepresentation()
        assert not repr.casegen
        assert repr.variation_name is None
        assert not repr.randgen
        assert repr.argument_name is None
        assert repr.argument_value is None

    def test_str(self):
        repr = ModifiersRepresentation()
        assert \
            str(repr) == \
                "ModifiersRepresentation(casegen: False randgen: No " + \
                "arg name: None arg value: None)"
    
    def test_short_desc(self):
        repr = ModifiersRepresentation()
        assert repr.short_description() == "No modifiers\n"

        repr.casegen = True
        assert repr.short_description() == "Modifiers:\n- case generation\n"

        repr.casegen = False
        repr.randgen = RandgenRepresentation()
        repr.randgen._present = True
        repr.randgen.name = "test"
        assert \
            repr.short_description() == \
                "Modifiers:\n- random generation: test (50%)\n"
        
        repr.randgen._present = False
        repr.argument_name = "test"
        assert \
            repr.short_description() == \
                "Modifiers:\n- argument name: test\n"
        
        repr.argument_name = None
        repr.argument_value = "test"
        assert \
            repr.short_description() == "Modifiers:\n- argument value: test\n"


class TestRandgenRepr(object):
    def test_default(self):
        repr = RandgenRepresentation()
        assert not repr
        assert not repr._present
        assert repr.name is None
        assert not repr.opposite
        assert repr.percentage == 50

    def test_bool(self):
        repr = RandgenRepresentation()
        assert not repr
        repr._present = True
        assert bool(repr)
    
    def test_str(self):
        repr = RandgenRepresentation()
        assert str(repr) == "No"

        repr._present = True
        repr.name = "name"
        assert str(repr) == "Yes 'name' (50%)"

        repr.opposite = True
        assert str(repr) == "Yes 'name' (opposite, 50%)"
