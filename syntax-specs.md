# Syntax specifications

## 1) Overview

*Chatette* is a Python script that can generate an input file for *Rasa NLU* from a file containing templates written in a Domain Specific Language. This document describes this DSL.

This DSL is a superset of *Chatito*'s DSL, described [here](https://github.com/rodrigopivi/Chatito/blob/master/spec.md).

Here is an example of such a template file.

```
; This template file defines examples of sentences people would say to introduce themselves
%[&introduce](2)
    ~[hi] ~[i am] @[name][, nice to meet you?]
    ~[hi] my name{'s/ is} @[name]

~[hi]
    hi
    hello
    howdy

~[i am]
    {i/I} am
    {i/I}'m

@[name]
    John
    Robert = Robert
    Bob = Robert
```

This will generate a file such as this one:
```json
{
  "rasa_nlu_data": {
    "common_examples": [
      {
        "entities": [
          {
            "end": 13,
            "entity": "name",
            "start": 7,
            "value": "Robert"
          }
        ],
        "intent": "introduce",
        "text": "Hi i'm Robert"
      },
      {
        "entities": [
          {
            "end": 19,
            "entity": "name",
            "start": 16,
            "value": "Robert"
          }
        ],
        "intent": "introduce",
        "text": "Howdy my name's Bob"
      }
    ],
    "entity_synonyms": [
      {
        "synonyms": [
          "Robert",
          "Bob"
        ],
        "value": "Robert"
      }
    ],
    "regex_features": []
  }
}
```

Template files can be encoded in either any charset, while JSON files will always be UTF-8 encoded.

## 2) Language syntax

As you can see in the example, a file is made of several definitions, made up of a declaration and a set of rules. The declaration is the unindented part, while the set of rules are indented. The indentation must be coherent inside a rule, i.e. each rule in a definition must be indented in the same way. However, different indentations may be used for different definitions.
