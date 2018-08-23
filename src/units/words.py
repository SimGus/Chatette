from units.units import *

from random import randint


class WordRule(Rule):
    """
    Represents a word inside a rule
    Accepted modifiers:
        - leading-space: bool
    """
    def __init__(self, word, leading_space=False):
    def __init__(self, name, leading_space=False, variation_name=None, arg_value=None,
        casegen=False, randgen=None, percentage_gen=None, parser=None):
            if variation_name is not None:
                raise SyntaxError("Words cannot have variations, yet '"+
                    name+"' does (unescaped '#'?)")
            if arg_value is not None:
                raise SyntaxError("Words cannot have an argument, yet '"+
                    name+"' does (unescaped ':'?)")
            if casegen:
                raise SyntaxError("Words cannot generate different cases, yet '"+
                    name+"' does (unescaped '&'?)")
            if randgen is not None or percentage_gen is not None:
                raise SyntaxError("Words cannot have a random generation modifier, yet '"+
                    name+"' does (unescaped '?'?)")
            if parser is not None:
                raise RuntimeError("Internal error: tried to create a word "+
                    "with a pointer to the parser")
            super(WordModel, self).__init__(name, leading_space=leading_space,
                                            variation_name=None, arg_value=None,
                                            casegen=False, randgen=None,
                                            percentage_gen=None, parser=None)
            self.word = name

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


class WordGroupRule(Rule):
    """
    Represents a word group token inside a rule
    Accepted modifiers:
        - leading-space: bool
        - casegen: bool
        - randgen: str
        - percentgen: bool
    """
    def __init__(self, name, leading_space=False, variation_name=None, arg_value=None,
        casegen=False, randgen=None, percentage_gen=50, parser=None):
            if variation_name is not None:
                raise SyntaxError("Word groups cannot have variations, yet '"+
                    name+"' does (unescaped '#'?)")
            if arg_value is not None:
                raise SyntaxError("Word groups cannot have an argument, yet '"+
                    name+"' does (unescaped ':'?)")
            if parser is not None:
                raise RuntimeError("Internal error: tried to create a word "+
                    "group with a pointer to the parser")

            super(WordGroupModel, self).__init__(name,
                                                 leading_space=leading_space,
                                                 variation_name=None,
                                                 arg_value=None,
                                                 casegen=casegen,
                                                 randgen=randgen,
                                                 percentage_gen=percentage_gen,
                                                 parser=None)
            self.words = name

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
