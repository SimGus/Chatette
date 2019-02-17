from chatette.units import UnitDefinition


class AliasDefinition(UnitDefinition):
    """
    This class represents the definition of an alias,
    containing all the rules that it can represent.
    """

    def __init__(self, name, modifiers, rules=None):
        super(AliasDefinition, self).__init__(name, modifiers, rules=rules)
        self.type = "alias"
    
    def _get_template_decl(self, variation=None):
        return '~' + super(AliasDefinition, self)._get_template_decl(variation)

    # Everything else is in the superclass
