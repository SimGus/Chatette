from chatette.units import UnitDefinition


class AliasDefinition(UnitDefinition):
    """
    This class represents the definition of an alias,
    containing all the rules that it can represent.
    """

    def __init__(self, name, modifiers, rules=[]):
        super(AliasDefinition, self).__init__(name, modifiers, rules=rules)
        self.type = "alias"

    # Everything else is in the superclass
