from units import *

from random import randint


class WordRule(TokenModel):
    """
    Represents a word inside a rule
    Accepted modifiers:
        - leading-space: bool
    """
    def __init__(self, word, leading_space=False):
        super(WordModel, self).__init__(word, leading_space=leading_space)
        self.word = word

    def generate_random(self, arg_value=None):
        if self.leading_space:
            return ' '+self.word
        return self.word

    def generate_all(self, arg_value=None):
        generated_examples = []
        if self.leading_space:
            generated_examples.append({
                "text": ' '+self.word,
                "entities": [],
            })
        generated_examples.append({
            "text": self.word,
            "entities": [],
        })
        return generated_examples


class WordGroupRule(TokenModel):
    """
    Represents a word group token inside a rule
    Accepted modifiers:
        - leading-space: bool
        - casegen: bool
        - randgen: str
        - percentgen: bool
    """
    def __init__(self, words_str, leading_space=False, casegen=False,
        randgen=None, percentage_gen=50):
            super(WordGroupModel, self).__init__(words_str, leading_space=leading_space,
                casegen=casegen, randgen=randgen, percentage_gen=percentage_gen)
            self.words = words_str

    def generate_random(self):
        if self.randgen is not None and randint(0,99) >= self.percentgen:
            return EMPTY_GEN

        # Generate the string according to the parameters of the object
        generated_str = self.words
        if self.casegen:
            generated_str = randomly_change_case(generated_str)
        if self.leading_space and may_get_leading_space(generated_str):
            generated_str = ' '+generated_str

        return {
            "text": generated_str,
            "entities": [],
        }

    def generate_all(self):
        generated_examples = []
        if self.randgen is not None:
            generated_examples.append("")

        if self.casegen:
            generated_examples.append(with_leading_lower(self.words))
            generated_examples.append(with_leading_upper(self.words))
        else:
            generated_examples.append(self.words)

        if self.leading_space:
            for (i, ex) in enumerate(generated_examples):
                if may_get_leading_space(ex):
                    generated_examples[i] = ' '+ex

        result = []
        for ex in generated_examples:
            result.append({
                "text": ex,
                "entities": [],
            })
        return result
