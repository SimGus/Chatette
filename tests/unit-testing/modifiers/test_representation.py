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
        representation = ModifiersRepresentation()
        assert not representation.casegen
        assert representation.variation_name is None
        assert not representation.randgen
        assert representation.argument_name is None
        assert representation.argument_value is None

    def test_str(self):
        representation = ModifiersRepresentation()
        assert \
            str(representation) == \
                "ModifiersRepresentation(casegen: False randgen: No " + \
                "arg name: None arg value: None)"

    def test_short_desc(self):
        representation = ModifiersRepresentation()
        assert representation.short_description() == "No modifiers\n"

        representation.casegen = True
        assert representation.short_description() == "Modifiers:\n- case generation\n"

        representation.casegen = False
        representation.randgen = RandgenRepresentation()
        representation.randgen._present = True
        representation.randgen.name = "test"
        assert \
            representation.short_description() == \
                "Modifiers:\n- random generation: test (50%)\n"

        representation.randgen._present = False
        representation.argument_name = "test"
        assert \
            representation.short_description() == \
                "Modifiers:\n- argument name: test\n"

        representation.argument_name = None
        representation.argument_value = "test"
        assert \
            representation.short_description() == "Modifiers:\n- argument value: test\n"


class TestRandgenRepr(object):
    def test_default(self):
        representation = RandgenRepresentation()
        assert not representation
        assert not representation._present
        assert representation.name is None
        assert not representation.opposite
        assert representation.percentage == 50

    def test_bool(self):
        representation = RandgenRepresentation()
        assert not representation
        representation._present = True
        assert bool(representation)

    def test_str(self):
        representation = RandgenRepresentation()
        assert str(representation) == "No"

        representation._present = True
        representation.name = "name"
        assert str(representation) == "Yes 'name' (50%)"

        representation.opposite = True
        assert str(representation) == "Yes 'name' (opposite, 50%)"
