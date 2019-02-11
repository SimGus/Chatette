from chatette.units import Example


class IntentExample(Example):

    def __init__(self, name, text=None, entities=None):# -> None:
        super(IntentExample, self).__init__(text, entities)
        self.name = name
    @classmethod
    def from_example(cls, name, ex):
        return cls(name, ex.text, ex.entities)

    # def __str__(self):
    #     return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name+self.text+str(self.entities))
