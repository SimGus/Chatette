from Unit import TokenModel

class WordModel(TokenModel):
    """Represents a word inside a rule"""
    def __init__(self, word, leading_space=False):
        super(WordModel, self).__init__(word, leading_space=leading_space)

    def generate_random(self):
        if self.leading_space:
            return ' '+self.name
        return self.name


class WordGroupModel(TokenModel):
    """Represents a word group token inside a rule"""
    def __init__(self, words_str, leading_space=False, casegen=False,
        randgen=False, percentage_gen=50):
            super(WordGroupModel, self).__init__(words_str, leading_space=leading_space,
                casegen=casegen, randgen=randgen, percentage_gen=percentage_gen)

    def generate_random(self):
        pass  # TODO manage randgen and stuff inside the super class
