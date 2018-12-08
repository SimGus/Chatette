from chatette.units import Example


class IntentExample(Example):

    def __init__(self, name, text="", entities=None):# -> None:
        super(IntentExample, self).__init__(text, entities)
        self.name = name

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
