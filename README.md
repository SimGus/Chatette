# *Chatette* dataset generator

![*Chatette* logo](/public/images/chatette-logo.png)

*Chatette* is a Python script that helps you generate training datasets for the [*Rasa NLU*](https://github.com/RasaHQ/rasa_nlu "rasa-nlu GitHub repository") Python package.
If you want to make large datasets of example data for Natural Language Understanding tasks without too much of a headache, *Chatette* is a project for you.

Specifically, *Chatette* implements a Domain Specific Language (*DSL*) that allows you to define templates to generate a large number of sentences. Those sentences are then saved in the input format of *Rasa NLU*.

The *DSL* used is a superset of the excellent project [*Chatito*](https://github.com/rodrigopivi/Chatito "Chatito's GitHub repository") created by Rodrigo Pimentel. (*Note: the DSL is actually a superset of Chatito v2.1.x for Rasa NLU, not for all possible adapters.*)

# How to use *Chatette*?

## Input and output data

The data that *Chatette* uses and generates is loaded from and saved to files. We thus have:
- The **input file** containing the templates.

   There is no need for a specific file extension. The syntax of the *DSL* to make those templates is described in the [syntax specification](syntax-specs.md).
   Note that templates can be divided into several files, with one *master* file linking them all together (described in the [syntax specification](syntax-specs.md)).

- The **output file**, a *JSON* file containing data that can be directly fed to *Rasa NLU*.

## Running *Chatette*

To run *Chatette*, you will need to have [Python](https://www.python.org/) installed.
*Chatette* works with both Python 2.x and 3.x.

Install `Chattete` via `pip`:
```bash
pip install chatette
```

Then simply run the following command:
```bash
python -m chatette.run <path_to_template>
```
or
```bash
python3 -m chatette.run <path_to_template>
```

You can specify the name of the output file as follows:
```bash
python -m chatette.run <path_to_template> -o <output_path.json>
```
or
```bash
python3 -m chatette.run <path_to_template> -o <output_path.json>
```
The output file will then be saved in a file named `output_path.json` within the same directory as the input file. If you didn't specify a name for the output file, the default one is `output.json`.

# *Chatette* vs *Chatito*?

A perfectly legitimate question could be:
> Why does *Chatette* exist when *Chatito* already fulfills the same purposes?

The reason comes from the different goals of the two projects:

*Chatito* aims at a generic but powerful *DSL*, that should stay simple. While it is perfectly fine for small projects, when projects get larger, this simplicity may become a burden: your template file becomes overwhelmingly large, at a point you get lost inside it.

*Chatette* defines a more complex *DSL* to be able to manage larger projects. Here is a non-exhaustive list of features that can help with that:

- Ability to break down templates into multiple files
- ~~Support for comments inside template files~~ (*Note: this is now possible in Chatito v2.1.x too*)
- Word group syntax that allows to define parts of sentences that might not be generated in every example
- Possibility to specify the probability of generating some parts of the sentences
- Choice syntax to prevent copy-pasting rules with only a few changes
- Ability to define the value of each slot whatever the generated example
- Syntax for generating words with different case for the leading letter
- Argument support so that some templates may be filled by given words
- Indentation must simply be somewhat coherent
- Support for synonyms

As previously mentioned, the *DSL* used by *Chatette* is a superset of the one used by *Chatito*. This means that input files used for *Chatito* are completely usable with *Chatette* (not the other way around). Hence, it is easy to get from *Chatito* to *Chatette*.

As an example, this *Chatito* data:
```
// This template defines different ways to ask for the location of toilets (Chatito version)
%[ask_toilet]('training': '3')
    ~[sorry?] ~[tell me] where the @[toilet#singular] is ~[please?]?
    ~[sorry?] ~[tell me] where the @[toilet#plural] are ~[please?]?

~[sorry]
    sorry
    Sorry
    excuse me
    Excuse me

~[tell me]
    ~[can you?] tell me
    ~[can you?] show me
~[can you]
    can you
    could you
    would you

~[please]
    please

@[toilet#singular]
    toilet
    loo
@[toilet#plural]
    toilets
```
could be directly given as input to *Chatette*, but this *Chatette* template would produce the same thing:
```
// This template defines different ways to ask for the location of toilets (Chatette version)
%[&ask_toilet](3)
    ~[sorry?] ~[tell me] where the {@[toilet#singular] is/@[toilet#plural] are} [please?]\?

~[sorry]
    sorry
    excuse me

~[tell me]
    ~[can you?] {tell/show} me
~[can you]
    {can/could/would} you

@[toilet#singular]
    toilet
    loo
@[toilet#plural]
    toilets
```

The *Chatito* version is arguably easier to read, but the *Chatette* version is shorter, which may be very useful when dealing with lots of templates and potential repetition.

Beware that, as always with machine learning, having too much data may cause your models to perform less well because of overfitting. While this script can be used to generate thousands upon thousands of examples, it isn't advised for machine learning tasks.

Note that *Chatette* is named after *Chatito*, as *-ette* in French could be translated to *-ita* or *-ito* in Spanish.

# Contributors

- [Vadim Fedorenko](https://github.com/meiblorn)

Many thanks to him!
