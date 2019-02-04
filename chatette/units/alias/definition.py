from chatette.units import UnitDefinition


class AliasDefinition(UnitDefinition):
    """
    This class represents the definition of an alias,
    containing all the rules that it can represent.
    """

    def __init__(self, name, rules=[], arg=None, casegen=False):
        super(AliasDefinition, self).__init__(name, rules=rules, arg=arg,
                                              casegen=casegen)
        self.type = "alias"
    
    def _get_template_decl(self, variation=None):
        return '~' + super(AliasDefinition, self)._get_template_decl(variation)

    # Everything else is in the superclass
