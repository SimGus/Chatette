# *Chatette* dataset generator &nbsp;&nbsp;&nbsp;&nbsp; [![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Chatette%3A+an+open-source+Python+package+to+easily+generate+datasets+for+Rasa+NLU&url=https://pypi.org/project/chatette&hashtags=rasa,rasaNLU,chatbots,conversationalAI)



<!--[![Github All Releases](https://img.shields.io/github/downloads/SimGus/Chatette/total.svg)](https://github.com/SimGus/Chatette)-->
[![PyPI package](https://badge.fury.io/py/chatette.svg)](https://badge.fury.io/py/chatette)
[![GitHub license](https://img.shields.io/github/license/SimGus/Chatette.svg)](https://github.com/SimGus/Chatette/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/SimGus/Chatette.svg?branch=master)](https://travis-ci.org/SimGus/Chatette)
[![codecov](https://codecov.io/gh/SimGus/Chatette/branch/master/graph/badge.svg)](https://codecov.io/gh/SimGus/Chatette)

![*Chatette* logo](https://raw.githubusercontent.com/SimGus/Chatette/master/public/images/chatette-logo.png)

*Chatette* is a Python script that generates training datasets for the Python package [*Rasa NLU*](https://github.com/RasaHQ/rasa_nlu "rasa-nlu GitHub repository") from template files.
If you want to make large datasets of example data for Natural Language Understanding tasks without too much of a headache, *Chatette* is a project for you.

Specifically, *Chatette* implements a Domain Specific Language (*DSL*) that allows you to define templates to generate a large number of sentences. Those sentences are then saved in the input format of *Rasa NLU*.

The *DSL* used is a superset of the excellent project [*Chatito*](https://github.com/rodrigopivi/Chatito "Chatito's GitHub repository") created by Rodrigo Pimentel. (*Note: the DSL is actually a superset of Chatito v2.1.x for Rasa NLU, not for all possible adapters.*)

# Installation
To run *Chatette*, you will need to have [Python](https://www.python.org/) installed.
*Chatette* works with both Python 2.7 and 3.x (>= 3.3).

*Chatette* is available on [PyPI](https://pypi.org/project/chatette), and can thus be installed using `pip`:
```sh
pip install chatette
```

**Alternatively**, you can clone the [GitHub repository](https://github.com/SimGus/Chatette) and install the requirements:
```sh
pip install -r requirements/common.txt
```
You can then run the module by using the commands below in the cloned directory.

# How to use *Chatette*?

## Input and output data

The data that *Chatette* uses and generates is loaded from and saved to files. We thus have:
- The **input file(s)** containing the templates.
  There is no need for a specific file extension. The syntax of the *DSL* to make those templates is described on the [wiki](https://github.com/SimGus/Chatette/wiki).

- The **output file**, a *JSON* file containing data that can be directly fed to *Rasa NLU*. It is also possible to use a *JSONL* format in the output.

## Running *Chatette*
Once installed, run the following command:
```bash
python -m chatette <path_to_template>
```
where `python` is your Python interpreter (some operating systems use `python3` as the alias to the Python 3.x interpreter).

You can specify the name of the output file as follows:
```bash
python -m chatette <path_to_template> -o <output_directory_path>
```

`<output_directory_path>` is specified relatively to the directory from which the script is being executed.
The output file(s) will then be saved in numbered `.json` files in `<output_directory_path>/train` and `<output_directory_path>/test`. If you didn't specify a path for the output directory, the default one is `output`.

Other program arguments and are described [in the wiki](https://github.com/SimGus/Chatette/wiki).

# *Chatette* vs *Chatito*?

A perfectly legitimate question is:
> Why does *Chatette* exist when *Chatito* already fulfills the same purposes?

The two projects actually have different goals:

*Chatito* aims at a generic but powerful *DSL*, that should stay simple. While it is perfectly fine for small projects, when projects get larger, this simplicity may become a burden: your template file becomes overwhelmingly large, to the point you get lost inside it.

*Chatette* defines a more complex *DSL* to be able to manage larger projects and tries to stay as interoperable with *Chatito* as possible.
Here is a non-exhaustive list of features *Chatette* has and that can help manage large projects:

- Ability to break down templates into multiple files
- Word group syntax that allows to modify the generation behavior of parts of sentences
- Possibility to specify the probability of generating some parts of the sentences
- Random generation of some parts of the sentences linked to that of other parts
- Choice syntax to prevent copy-pasting rules with only a few changes
- Ability to define the value of each slot whatever the generated example
- Syntax for generating words with different case for the leading letter
- Argument support so that some templates may be filled by different strings in different situations
- Indentation is permissive and must only be somewhat coherent
- Support for synonyms

As the *Chatette*'s DSL is a superset of *Chatito*'s one, input files used for *Chatito* are completely usable with *Chatette* (not the other way around). Hence, it is easy to get from *Chatito* to *Chatette*.

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
could be directly given as input to *Chatette*, but this *Chatette* template would produce the same results:
```
// This template defines different ways to ask for the location of toilets (Chatette version)
%[&ask_toilet](3)
    ~[sorry?] ~[tell me] where the {@[toilet#singular] is/@[toilet#plural] are} [please?]?

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

# Development
For developers, you can clone the [repo](https://github.com/SimGus/Chatette) and install the development requirements:

```pip install -r requirements/develop.txt```

Run pylint:

```tox -e pylint```

Run pycodestyle:

```tox -e pycodestyle```

Run pytest:

```tox -e pytest```

You can also install the module as editable using `pip`:
```sh
pip install -e <path-to-cloned-repo>
```
You can then run *Chatette* as if you installed it from PyPI.

# Credits
## Author and maintainer
- [SimGus](https://github.com/SimGus)

*Disclaimer: This is a side-project I'm not paid for, don't expect me to work 24/7 on it.*

## Contributors
- [Vadim Fedorenko](https://github.com/meiblorn)

Many thanks to him!
