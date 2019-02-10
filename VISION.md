# Vision
In this file, we will present the "vision" behind *Chatette*. In other words, this file will explain:
- the general aim and important points that should be kept in mind when developing this program
- big milestones that would be worth reaching in the future
- big problems that can only be solved by breaking back compatibility

## General aim
*Chatette* is intended to be used by chatbot developers (even though it could be useful in other situations).
The point of it is to be able to quickly generate lots of example sentences that can be used to train the NLU model of a chatbot. The developer should have control over what kind of examples are generated (especially since it is not possible to check by hand that all generated examples are correct).

## Important points
All the points described in this section are not features but rather subject that we should keep focusing on when searching for ideas of new features. Adding, modifying or removing a feature should always be done while having those points in mind.

### Interoperability with *Chatito*
*Chatette* was first envisioned as a replacement tool for [*Chatito*](https://github.com/rodrigopivi/Chatito). This project indeed lacks (or at least lacked) several features that would make the life of a chatbot developer easier. The top three lacking functionalities definitely were:
- the ability to break template files into several files
- the ability to put comments in template files (*this is now supported in *Chatito**)
- a less severe parser when it comes to indentation (*Chatito* doesn't allow other indentation styles than 4 spaces)

Therefore, a key feature of *Chatette* should be to stay **as compatible as possible with Chatito's input files**. This way, this project can be a drop-in replacement to *Chatito* in a *Rasa* project. To be exact, all relevant features in the DSL of *Chatito* should be understood by *Chatette*.

### Prevent overfitting
As *Chatette* is intended to produce training (and testing) datasets for machine learning tasks, it is important to keep in mind that overfitting is a recurring problem in that kind of tasks.
When adding or modifying features, we should always try to **make overfitting unlikely to happen given the template inputs**.

Obviously, this is not an easy tasks; we should thus at least try not to make overfitting more likely to happen.

This is notably related to [this problem](#over-representation-of-high-variability-example-sentences).

### Prevent duplication of syntax
*Chatette* defines a Domain-Specific Language that is used to make templates. This DSL is the same as that of *Chatito* with added syntax for additional functionalities.
When adding or modifying syntax of this DSL, we should **prevent having different ways of describing the same templates**. If we have 2 ways of describing a template, we should rather keep the shortest one, unless it is extremely hard to read.

### Keep a balance between short and readable
The DSL of *Chatette*, on the contrary as that of *Chatito*, generally aims at making shorter template files. Indeed, when you look at input files for *Chatito*, there is quite a lot of repetition in them. However, those files are also very readable (from the point of view of someone who would not know the DSL very well).

While a DSL aimed at short templates would help developers create them quicker, readability is obviously a very nice quality of such a DSL.

It is thus importance to try and **define a DSL that is as short as possible while staying as readable as possible** for the non-initiated.

### Prevent breaking backwards-compatibility within the DSL
As users most likely wrote their template files once and wouldn't want to rewrite them all over again on each minor patch of *Chatette*, we should **avoid making changes that break previously working template files**. This is true for both the syntactic validity of a template file, and the generation behavior of *Chatette* when dealing with a template file.

As we use SemVer 2.0.0, backward-incompatible changes should be done only when changing the major version number (thus for now, when moving from versions 1.x.x to 2.0.0).

It should only be allowed to change the behavior of the parser and the generator if this fixes a bug and the previous behavior was neither intended or documented in the documentation.

## Future features
We describe here large features that would be worth adding to *Chatette*.

### Predefined aliases and slots
A lot of aliases and slots are quite common amongst chatbots. In a lot of chatbot frameworks, common types of entities are provided to be used by the developer.
If you don't use such a framework, you will need to define those entities by yourself.
It would thus be nice to have a set of predefined aliases and slots that would be usable when creating templates.

Common aliases and slots notably are:
- first names
- last names
- dates (in different formats)
- cities
- numbers (in different formats)
- lots of others

We could go as far as making all those slots multilingual thanks to variations modifiers.

## Current problems

### Duplication of functionalities between word groups and choices
While word groups can just contain words, it turns out choices can do quite the same thing, with additional functionalities.

Here is a table that summarizes the point and characteristics of both sub-rules:

| Characteristic | Word groups | Choices |
|----------------|-------------|---------|
| Point          | Quick way to define parts of the sentence that can get a modifier | Quick way to tell the generator to choose between different rules
| Can contain    | Words       | Any sub-rule |
| Accepted modifiers | - Case generation                  | - Case generation
|                    | - Named random generation          | - Unnamed random generation
|                    | - Percentage for random generation |

This shows both sub-rule types are highly similar and could be merged into just one.
As choices are the only thing that uses curly braces as special characters, the proposition would be to merge the functionalities of choices into word groups.

This change wouldn't break back-compatibility until we decide to completely remove choices and use curly braces for something else.

### Over-representation of high variability example sentences
Currently, when a rule in a unit definition has a high variability (meaning it can potentially generate lots of different sentences), it gets selected more often than other rules. Some rules are thus over-represented in the generated examples, leading to possible overfitting.

Making changes to the DSL should fix that, but it seems *Chatito* is dealing with the same problem. Waiting for their change would thus make sense.
