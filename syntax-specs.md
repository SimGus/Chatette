# Syntax specifications

## 1. Overview

*Chatette* is a Python script that can generate an input file for *Rasa NLU* from a file containing templates written in a specific Domain Specific Language. This document describes this DSL.

The DSL is a superset of *Chatito* v2.1.x's DSL (with the *Rasa NLU* adapter), described [here](https://github.com/rodrigopivi/Chatito/blob/master/spec.md). (To be totally exact, as *Chatette*'s DSL defines a little more special characters and is thus not exactly a superset of *Chatito*'s DSL in the sense that a rather small number of template files that would work with *Chatito* would not be valid in *Chatette*. Conversely, a lot of files that would be valid inputs for *Chatette* wouldn't be valid for *Chatito*.)

Here is an example of a template file *Chatette* could use as an input file.

```
// This template file defines examples of sentences people would say to introduce themselves
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

The generated file will contain a training dataset and will thus look as the one shown hereafter. This data is made up of examples sentences which are labelled as having a certain intent and optionally contain one or several entities corresponding to the value of a slot. There is also a support to list synonyms for entity value. Read about *Rasa NLU*'s data format [here](http://rasa.com/docs/nlu/0.13.1/dataformat/) for more information.
```json
{
  "rasa_nlu_data": {
    "common_examples": [
      {
        "text": "Hi i'm Robert",
        "intent": "introduce",
        "entities": [
          {
            "end": 13,
            "entity": "name",
            "start": 7,
            "value": "Robert"
          }
        ]
      },
      {
        "text": "Howdy my name's Bob",
        "intent": "introduce",
        "entities": [
          {
            "end": 19,
            "entity": "name",
            "start": 16,
            "value": "Robert"
          }
        ]
      }
    ],
    "entity_synonyms": [
      {
        "value": "Robert",
        "synonyms": [
          "Robert",
          "Bob"
        ]
      }
    ],
    "regex_features": []
  }
}
```

Template files can be encoded in any charset, while JSON files will always be UTF-8 encoded.

You can find other illustrative examples at the end of this document.

## 2. Language syntax

As visible in the example shown above, a file is composed of several **definitions**, made up of what we will call a **declaration** and a **set of rules**, one rule per line.
The declaration is the unindented part, while the set of rules are indented. The indentation must be coherent inside a rule, i.e. each rule in a definition must be indented in the same way. However, different indentations may be used for different definitions.

In the declaration, in-between square brackets, you can see the identifier of a definition. This identifier is the name used to refer to this particular definition.
Note that a declaration doesn't have to be made before being referenced and doesn't even have to be located in the same file as its references, as long as the declaration exists somewhere.

Identifiers can be made of any characters, including whitespaces. The only forbidden characters are the line feed (`\n`) and carriage return (`\r`), since they are used to separate rules and definitions.

Some modifiers may be added to declarations to affect what they will generate. Those modifications are made using special characters, put besides the identifier (inside the brackets).

Everything that follows two slashes (`//`) is considered to be a comment and is thus ignored. Using a semi-colon `;` instead of those two slashes to annouce comments is now deprecated (a warning will be printed if this is used) but will still work until version 2.0 is out. Empty lines are ignored as well.

The structure of such a file can thus be represented as follows:
```
// Whole line comment
DECLARATION1
    RULE1
    RULE2

DECLARATION2  // Other comment
  RULE1
  RULE2
```

If you want to use special characters (semi-colons, square brackets, etc.) as normal characters, they should be escaped by prepending a backslash (`\`) to them in order to avoid incorrect parsings of the templates. This is true anywhere in the template documents, except in comments.

Here is an exhaustive list of characters which should be escaped:

|   |   |
|---|---|
| Semi-colon | `;` |
| Percent | `%` |
| Tilde | `~` |
| At | `@` |
| Question mark | `?` |
| Hashtag | `#` |
| Slash | `/` |
| Dollar sign | `$`
| Ampersand | `&` |
| Square brackets | `[` and `]` |
| Curly braces | `{` and `}` |
| Equal symbol | `=` |
| Pipe | `\|` |
| Backslash | `\` |
| Double slash | `//` |

Note that not escaping these characters might not be problematic in certain cases, but it is more prudent to do so in all cases. Escaping a character outside of this list will simply be ignored by the parser which will act as if there was no backslash there.

Let's now review what rules are, before looking closer to declarations.

### 2.1. Rules

As we said, a definition contains a set of rules, indented and separated by new lines.
A rule is made of "tokens" which are either words (or group of words) or references to other definitions.
A rule is used to generate an example: one after the other each token of the rule, being able to generate one or several words, generates them. This sequence of words is then concatenated to result in the string generated by the rule.
Notice that the generation of most of those tokens can be adapted using modifiers.

We list and explain each and every possible token hereafter.

#### 2.1.1. Words

Words are tokens that can only generate one word. This kind of token cannot take any modifier.

For example, the rule `this is a rule`, which contains 4 word tokens, will *always* generate the sentence `this is a rule`.

#### 2.1.2. Word groups

Word groups are tokens that are a little more adaptable. As the name suggests, they are a group of words grouped within square brackets.
Such tokens will generate the exact string that is enclosed in the square brackets, unless some modifiers adapts their generation.

A word group can take three modifiers:

- A **case generation** modifier (in short *casegen*)

  Adding an ampersand `&` as the first character in the square brackets will make the word group choose at random to generate its leading letter as either an uppercase or lowercase letter. This will work even if the word group begins with non-letter characters: the leading letter is then the first letter character.

  For example, the word group `[&hello I'm a test]` will generate `hello I'm a test` 50% of the time and `Hello I'm a test` 50% of the time.

- A **random generation** modifier

  Adding a question mark `?` after the word group's string will make the word group either generate something or nothing, at random.

  For example, `[test?]` will generate `test` 50% of the time and nothing 50% of the time.

  It is possible to give a name to such a modifier. Then, each token that will have a random modifier with the same name in the rule will generate something if and only if the other tokens with the same modifier generated something, and vice-versa.

  For example, the rule `Hey [I'm a?name] pretty [test?name]` will generate either `Hey I'm a pretty test` or `Hey pretty`, but *never* `Hey I'm pretty` or `Hey pretty test`.

- A **percentage for the random generation** modifier

  When adding a random generation modifier as shown above, the generation defaults to generating the string 50% of the time and not generating it 50% of the time. These numbers can be changed by giving the percentage of the time the token should generate something, without the percent symbol `%` and separated from the random generation modifier by a slash `/`.

  Thus, the rule `[test?/80]` will generate `test` 80% of the time, and will generate nothing 20% of the time.

  Of course, a name for the random generation can still be provided between the question mark and the slash.

#### 2.1.3. Alias references

Aliases are references to alias definitions that are made in other parts of the file (or even in other files, as we will see later).
Those definitions contain rules that can generate a string (or potentially nothing).
When we reference an alias in a rule, we are actually asking the generator to choose one of the rules in the definition of this alias, make it generate a string and replace the reference by this string.

Note that if you have circular references in your template (a reference within a definition that references another definition containing a reference to the current definition for example), the generator will loop forever without warnings. This is true for any kind of reference.

An alias reference begins with a tilde `~`, followed by the identifier of the alias in-between square brackets, such as `~[alias identifier]`.

For example, with the following alias definition:
```
// Definition of the alias named "hello"
~[hello]
  Hello
  Hi
```
the following rule will generate either `Hello` or `Hi`.
```
// The rule
    ~[hello]
```

As word groups, the string generation of aliases can be adapted by using modifiers. Not only can alias references take the same modifiers as word groups, i.e. the **case generation** modifier `&`, the (possibly named) **random generation** modifier `?` and its **probability of generation** `/`, but it can also take the following modifiers:

- A **variation name**

  As will be explained later, it is possible to define the same alias with several different variations. This is for example useful when you want to define a certain alias in a singular and in a plural form.
  Each variation thus has a name, which can be refered to by appending a hashtag `#` to the identifier of the alias and writing the name of the variation after that.

  For example, we could have the alias references `~[to be#singular]` and `~[to be#plural]`. If you don't specify a variation for this reference, the generator will consider all the rules from all the variations of this alias.

- An **argument value**

  It is sometimes useful to be able to give an argument to an alias definition when it is used. The argument value is thus a string that will be used inside the alias definition. This string must be written after a dollar sign `$` before the closing square bracket.

  For example, if we have an alias definition named `greet` that would generate `hello $NAME!`, where `$NAME` identifies the argument, the alias reference `~[greet$John]` in a rule will generate `hello John!`.

#### 2.1.4. Slot references

Slots references are pointers to slot definitions made somewhere else. The difference with an alias reference is that the string generated by a slot will be marked as an *entity*, i.e. the value of a slot. See [*Rasa NLU*'s doc](http://rasa.com/docs/nlu/0.13.2/entities/) for more information about what entities represent.

A slot reference begins with an at sign `@` followed by the identifier (and possibly modifiers) between square brackets, as for alias references.
Slot references can take the same modifiers as alias references.

#### 2.1.5. Intent references

As for alias and slot references, intent references refer to intent definitions made somewhere else. An intent reference, used in a rule, is totally equivalent to an alias reference (except it references an intent definition rather than an alias definition). The difference between an alias definition and an intent definition will be explained later on in this document.

Intent references begin with a percent symbol `%`. Their identifier must be in-between brackets as for alias and slot references.
Intent references take the same modifiers as alias and slot references.

#### 2.1.6. Choices

Choice tokens are a way to quickly say to the generator to choose between 2 "sub-rules" to generate in a rule. A choice token is a list of choice items separated by slashes `/`, all this in-between curly braces (`{` and `}`).

A choice item may be any kind of valid rule.
Beware that spaces are considered meaningful characters, which means putting a space before or after a slash symbol will generate a space if the right token is chosen. Also, as for all tokens, you cannot put a newline inside it (it would be considered to be the beginning of a new rule).

For example, the choice `{hello/hi/hey}` will generate `hello` 33% of the time, `hi` 33% of the time and `hey` 33% percent of the time.

Choices can take 2 modifiers:
- A **case generation** modifier

  This modifier has the exact same behavior as for word groups, alias, slot and intent references. It is denoted with an ampersand `&` at the beginning of the choice (right after the opening curly brace).

- An **unnamed random generation** modifier

  This modifier has the same behavior as we explained earlier, except it is not allowed to name it. The random generation modifier is indicated with a question mark `?` at the very end of the choice, right before the closing curly brace.

Note that you can use any of the token type we talked about in the previous subsections and adapt them with the modifiers they can take.
Therefore, the choice `{hi [my name is?/20] Jeff/hello [i'm?/30] Jeff}` is a totally valid choice, that will generate `hi Jeff` 40% of the time, `hi my name is Jeff` 10% of the time, `hello Jeff` 35% of the time and `hello i'm Jeff` 15% of the time.

As choices are not very readable, it is not advised to use them to choose between a large number of choice items or between very long items. Indeed, the same generation behavior is achievable by specifying several different rules in the current definition.

### 2.2. Definitions and declarations

As we said, each definition starts with a declaration. Declarations are begin with a special character to distinguish the different types of definitions, followed by their identifier in-between square brackets. Those special characters are the same we used for references, i.e. a tilde `~` for aliases, an at sign `@` for slots and a percent symbol `%` for intents.

As for references, it is possible to add modifiers between the brackets.
For declarations, three modifiers are supported:

- **Case generation**

  Adding an ampersand `&` as the first character in-between the brackets will make the string generated by this definition have either an uppercase or lowercase leading letter, at random, regardless of the modifiers for the reference. What this means is that, when a rule uses a reference to this definition (may this reference have a case generation modifier or not), the string that will replace this reference will always randomly choose to begin with an uppercase or a lowercase letter.

- **Variation naming**

   As we explained for references, putting a hashtag `#` after the identifier of a definition allows to give it a "sub-name" that would precise the definition. When several definitions have the same identifier but different variation names, those names can be used to reference the different definitions. Using a reference with the identifier alone (without any variation name) will reference all those different definitions as if they had been all one and only one definition with all the rules inside it. This is what makes this different from simply defining several definitions with different identifiers.

   A good example of such a use is to have a "singular" variation and a "plural" variation, which would be useful in certain cases, and in others you wouldn't care to have a singular or a plural and would need another definition with both singular and plural variaties if variations didn't exist.

   The hashtag must be placed after the declaration name and the variation identifier must be placed after the `#`. An empty variation name is not allowed.

- **Argument name**

    This modifier allows to tell that certain parts of the rules can be replaced by one or several words provided at reference time. This is very useful when you have two definitions that would contain all the same rules if there wasn't a certain word inside them that was different for each rule.

    The dollar sign `$` must be placed after the declaration name and the identifier and the argument has to be located after that. As for any other identifiers, arguments identifiers can be made up of any characters except line breaks (and special characters should be escaped). In the example, we usually use uppercase arguments name to quickly spot them.

    Inside rules, you would reference the argument simply by writing it, prepended by a dollar sign.
    For example:
    ```
    ~[greet$NAME]
        hello $NAME
    ```

Let's now review the differences between the three types of definitions.

#### 2.2.1. Alias definitions

Aliases are the simplest kind of definition: they are simply a "handle" (i.e. a way to reference) a set of rule. As we said, when referencing an alias in a rule, we are actually asking the generator to choose one and only one rule within this set of rules and to replace the reference by the generated string.

#### 2.2.2. Slot definitions

As we already said, slot references refer to slots definitions in the same way alias references refer to alias definitions. Of course, there is a difference: when a slot reference generates a string, the generator adds an entity in the entities list of the generated example in the output file.

For example, with a slot defined as
```
@[name]
    James
```
here is what the rule `Hi @[name]` could generate:
```json
{
  "rasa_nlu_data": {
    "common_examples": [
      {
        "text": "Hi James",
        "intent": "example",
        "entities": [
          {
            "end": 7,
            "entity": "name",
            "start": 3,
            "value": "James"
          }
        ]
      }
    ],
    "entity_synonyms": [],
    "regex_features": []
  }
}
```

To have more information about what entities represent in *Rasa NLU*, refer to its  [documentation](http://rasa.com/docs/nlu/0.13.2/entities/).

As you can see, an entity has a value. By default, the value will be the string generated for the slot (in the case above `James` was generated, the entity value will thus be `James`). It is however also possible to define another value for the entity, which will then also define synonyms.

It is useful when the slot is able to generate several different strings which would map to the same value. For example, let's say we have an intent `~[astronaut]` defined as follows:
```
~[astronaut]
    astronaut
    cosmonaut
    spaceman
```
This alias would be used in a slot `@[job]`. You would thus certainly like that whichever string is generated, the dataset still shows the same value for all these strings. In other words, having `astronaut`, `cosmonaut` or `spaceman` in the example should all map to the same entity value, so that the NLU model trained on the dataset recognizes all those strings as meaning the same thing.

If we wanted to have `astronaut` as the entity value for all those strings, we would have two ways to do so:
```
@[job]
    ~[astronaut] = astronaut
    // other rules
```
Here all strings generated by the rule (whatever the number of tokens in the rule) will take `astronaut` as entity value. Of course, any value can be put after the equal sign `≃`.

The other way to do this is the following:
```
@[job]
    ~[astronaut] = /
    // other rules
```
Here all strings generated by the first rule (once again, whatever the number of tokens in it) will take as entity value the identifier of the first token of the rule (thus here, `astronaut`). If the first token is a word, the entity value will be the word; if it is a word group, the entity value will be the group of words enclosed in the brackets; if it is a choice, the entity value will be the string enclosed within the curly braces (which is likely not the expected behavior).

Doing this kind of things will also fill up the synonyms list in the output file: `cosmonaut` and `spaceman` will be marked as synonyms for `astronaut`. Refer to [*Rasa NLU*'s documentation](http://rasa.com/docs/nlu/0.13.2/dataformat/#entity-synonyms) for the format and required pipelines used for entity synonyms.

#### 2.2.3. Intent definitions

Finally, let's talk about intent definitions.
As we said, when used within a rule, intent references behave exactly as alias reference.

The only difference between alias and intent definitions is that the definition of an intent (and *not* its use in rules) is a handle for the generator. In other words, intent definitions are entry points to the generation.

An intent definition can indeed be followed by a number in-between parentheses. This number specifies to the generator how many example sentences with this intent should be generated.

For example, the following intent definition tells the generator to generate 10 example sentences with intent `greet`.
```
%[greet](10)
    ~[hello] @[name]!
```

Another syntax (from *Chatito v2.1.x*) can also be used to define the number of examples asked. The intent declaration would be followed by several arguments with the following syntax: `'argument': 'value'` (arguments being separated by commas). The argument name for asking for a certain number of examples is `'training'` (the value is the number of examples in-between single quotes).

This syntax allows to support the generation of training and testing datasets: with the additional `'testing'` argument, you can ask for the generation of another file containing examples that are not in the first file (if it is possible). This second file can thus be used to evaluate the model you would have trained on the first file. By default, this second file will be named `testing-dataset.json`.

For example, this intent definition would generate 5 examples with intent `greet` in the training dataset and 2 other examples with the same intent (if they exist) in the test dataset.
```
%[greet]('training': '5', 'testing': '2')
    ~[hello]
```

### 2.3. Other special syntax

There is one more feature that *Chatette* has and which we can talk about: file inclusion.
When working on large projects, it is very useful to be able to divide data into different files. This also holds for template files, as they can grow very large with the size of the project.

What the DSL allows to do is thus to have a "master" file, that would be given as input to *Chatette*, and you would put references to other files within this file. The syntax to do so is the following: simply specify the path of the file you want to reference on a line and prepended by a pipe `|`. Those paths have to be relative to the master file.

To be exact, when the parser reads such a command, it actually includes (and reads) the contents of the referenced file at this spot in the master file.

Note that it is possible to include files within other files than the master file.

## 3. Illustrative examples

In this section, we will show an illustrative example, made for the following case: a dataset that defines examples for a simple conversation with a chatbot. The user's messages are divided into three intents: a greeting intent (for when the user says hello to the bot), an inform mood intent (for when the user says they're fine or not) and a goodbye intent.
The templates will be divided into two files, as you will see. Note that the extension of the files is `.chatette`, which is a usual extension for template files for *Chatette* but not mandatory.

`master-file.chatette`
```
// Master file defining the intents
%[&greet](2)
    ~[hello][!?]

%[&inform-mood](5)
    [well?] [&i]{~[am#elision]/ ~[am#no elision]} @[mood#good][!?] [:)?]
    [well?] [&i]{~[am#elision]/ ~[am#no elision]} @[mood#bad][...?]
    [&i] feel @[mood#good][!?] [:)?]
    [&i] feel @[mood#bad][...?]

%[&goodbye](2)
    ~[bye][!?]

|aliases-and-slots.chatette
```

`aliases-and-slots.chatette`
```
// File defining the aliases and slots
~[hello]
    hello
    hi

~[am#elision]
    'm
    've been
~[am#no elision]
    am
    have been

~[bye]
    bye
    goodbye
    see you

@[mood#good]
    good
    fine = good
    great = good
@[mood#bad]
    bad = /
    not so good = bad
    terrible = bad
```

This example would generate a dataset such as this:
```json
{
  "rasa_nlu_data": {
    "common_examples": [
      {
        "entities": [
          {
            "end": 12,
            "entity": "mood",
            "start": 7,
            "value": "good"
          }
        ],
        "intent": "inform-mood",
        "text": "i feel great! :)"
      },
      {
        "entities": [
          {
            "end": 18,
            "entity": "mood",
            "start": 15,
            "value": "bad"
          }
        ],
        "intent": "inform-mood",
        "text": "well i've been bad..."
      },
      {
        "entities": [
          {
            "end": 10,
            "entity": "mood",
            "start": 7,
            "value": "bad"
          }
        ],
        "intent": "inform-mood",
        "text": "i feel bad..."
      },
      {
        "entities": [
          {
            "end": 11,
            "entity": "mood",
            "start": 7,
            "value": "good"
          }
        ],
        "intent": "inform-mood",
        "text": "i feel fine! :)"
      },
      {
        "entities": [
          {
            "end": 15,
            "entity": "mood",
            "start": 4,
            "value": "bad"
          }
        ],
        "intent": "inform-mood",
        "text": "i'm not so good"
      },
      {
        "entities": [],
        "intent": "goodbye",
        "text": "goodbye"
      },
      {
        "entities": [],
        "intent": "goodbye",
        "text": "see you"
      },
      {
        "entities": [],
        "intent": "greet",
        "text": "Hello!"
      },
      {
        "entities": [],
        "intent": "greet",
        "text": "hi"
      }
    ],
    "entity_synonyms": [
      {
        "synonyms": [
          "bad",
          "not so good",
          "terrible"
        ],
        "value": "bad"
      },
      {
        "synonyms": [
          "good",
          "fine",
          "great"
        ],
        "value": "good"
      }
    ],
    "regex_features": []
  }
}
```

As usual with *Rasa NLU*'s dataset, it is advised to look at them within a tool rather than to read the JSON file directly (as it is less easy to read this way). You can use the very good project [*Rasa NLU* trainer](https://rasahq.github.io/rasa-nlu-trainer/) for this.
