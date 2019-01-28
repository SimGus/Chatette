"""
Module `chatette.modifiers.representation`
Contains structures that represent the possible modifiers
that could apply to unit declarations or sub-rules.
"""

class BaseModifiersRepr(object):
    def __init__(self, case_generation=False):
        # `case_generation` is a bool
        self.casegen = case_generation

class UnitDeclarationModifiersRepr(BaseModifiersRepr):
    def __init__(self, case_generation=False, variation_name=None,
                 argument_name=None):
        super(UnitDeclarationModifiersRepr, self).__init__(case_generation)
        self.variation_name = variation_name
        self.argument_name = argument_name

class WordGroupModifiersRepr(BaseModifiersRepr):
    def __init__(self, case_generation=False, randgen_name=None,
                 percentage_randgen=50):
        super(WordGroupModifiersRepr, self).__init__(case_generation)
        self.randgen_name = randgen_name
        self.percentage_randgen = percentage_randgen

class ChoiceModifiersRepr(BaseModifiersRepr):
    def __init__(self, case_generation=False, randgen=False):#,
                #  percentage_randgen=50):
        super(ChoiceModifiersRepr, self).__init__(case_generation)
        self.randgen = randgen
        # self.percentage_randgen = percentage_randgen

class ReferenceModifiersRepr(BaseModifiersRepr):
    def __init__(self, case_generation=False, randgen_name=None,
                 percentage_randgen=50, variation_name=None,
                 argument_value=None):
        super(ReferenceModifiersRepr, self).__init__(case_generation)
        self.randgen_name = randgen_name
        self.percentage_randgen = percentage_randgen
        self.variation_name = variation_name
        self.argument_value = argument_value
