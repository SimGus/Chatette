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
            self.words = words_str

    def generate_random(self):
        if self.randgen and randint(0,99) >= self.percentgen:
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
        if self.randgen:
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
