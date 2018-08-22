from Unit import *

from random import randint


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
        if self.randgen and randint(0,99) >= self.percentgen:
            return EMPTY_GEN

        # Generate the string according to the parameters of the object
        generated_str = self.words_str
        if self.casegen:
            generated_str = andomly_change_case(generated_str)
        if self.leading_space and may_get_leading_space(generated_str):
            generated_str = ' '+generated_str

        return {
            "text": generated_str,
            "entities": [],
        }
