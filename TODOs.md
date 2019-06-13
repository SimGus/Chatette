# TODOs

- [ ] parse in a better way asked number of generation of intents
- [ ] accept `#` as intent symbol (as well as `%` currently) to get closer to IBM Watson's syntax
- [ ] add some kind of optional version number within template files
- [ ] add a way to specify a rule on several consecutive lines
- [ ] add a way to give several different names to units
- [ ] add a way to force a rule at least once in the training/testing set

- [ ] add an adapter to output raw lists of questions (rather than a JSON file) (without entities?)
- [ ] add an adapter for *Rasa markdown*
- [ ] add an adapter for *Snips* (cf. Chatito)
- [ ] add an adapter for *Google DialogFlow*
- [ ] add an adapter for *IBM Watson*
- [ ] add an adapter for *Microsoft LUIS* as described [here](https://github.com/rodrigopivi/Chatito/issues/61) (cf. Chatito)
- [ ] add default aliases and slots

- [ ] add opposite `randgen` names
- [ ] support several arguments in one rule
- [ ] reverse regex
- [ ] add probabilities of generation for rules in defintions (cf. https://github.com/rodrigopivi/Chatito/issues/48 and new implementation) 
- [ ] add support for Chatito's augmentations (cf. https://github.com/rodrigopivi/Chatito/issues/48)
- [ ] add an annotation for generating typos
- [ ] add a flag to enable/disable the slot = slot synonym behavior (cf. https://github.com/rodrigopivi/Chatito/issues/50)
- [ ] add a way to make some generation mandatory in the training set, test set or both (cf. https://github.com/rodrigopivi/Chatito/issues/51)
- [ ] add custom annotations as *Chatito* does
- [ ] add support for any sub-rule's modifier for choices
- [ ] make double quotes an ignored character in annotations
- [ ] accept anything inside an arg, especially unit references
- [ ] add percentages of all possible examples for training and test (rather than simple numbers)

- [ ] add regex to rasa JSON file

- [ ] add a command line option to specifiy the max number of examples to generate
- [ ] add bulk generation
- [ ] add program options to change the names of the output files
- [ ] add a command line option to run in case insensitive

- [ ] design patterns
- [ ] make the division between processing and lookup more important in parser
- [ ] improve logging (remove `print`s and use a logging library)
<!-- - [ ] rewrite docstrings formatted as explained in *PEP257* -->
- [ ] detect and warn about circular references
- [ ] warn if there are slots within slots
- [ ] warn if the limit of examples generated was reached
- [ ] warn if a unit reference is used within its own declaration
- [ ] warn if an argument has no value
- [ ] check that intent definitions don't overlap
- [ ] cache the possible number of generatable examples for each unit
- [ ] use multithreading or multiprocessing to optimize the execution time (+ program option to set that on/off)

- [ ] replace `getcwd` by `six.moves.getcwd` to be sure to have python 2 and 3 compliant code
- [ ] replace `print` by `six.print_`?
- [ ] replace `range` by `six.moves.range`
- [ ] replace `zip` by `six.moves.zip`

- [ ] complete refactor of the code: the code is almost unmaintainable
- [ ] refactor units to remove duplicated code: make modifiers act after the string has been generated
- [ ] add more unit tests

- [ ] *Interactive mode* add support for argument values in relevant commands
- [ ] *Interactive mode* use `tabulate` to make tables and make command output more readable

- [ ] *Docs* clearly state the objective (scope) of the program
- [ ] *Docs* add a "contributors" part
- [ ] *Docs* add a representation of the architecture of the project
- [ ] *Docs* multilingual
- [ ] *Docs* specify which version of *Rasa NLU* *chatette* can work with
- [ ] *Docs* explain that redefining a unit silently appends the rules to the already declared unit (with the same modifiers as the first time)
- [ ] *Docs* document the differences between *Chatito* and *Chatette*
- [ ] *Docs* make docs available from `help()` function

- [ ] add sections in TODO list to make it more readable
- [ ] make an installer to use the script directly from the command line (at least in *nix systems)

## Done

- [x] fix line number count for different files
- [x] add unicode support for all files (`io.open` autodetects encoding i think)
- [x] add argument support
- [x] generate all possible sentences when asked
- [x] add synonyms into the synonym object of rasa JSON file
- [x] fix overriding of rules
- [x] add entities when generating slot in OOP rewriting
- [x] add *casegen* inside declarations
- [x] add choice support in *OOP* rewriting
- [x] slot value should be the whole text and not only the first word if no value is given
- [x] remove escapement in slot values
- [x] add a `choose` function utility
- [x] give a default nb of indent for `printDBG` methods
- [x] add support for synonyms in OOP rewriting
- [x] check that slot value in slots content has any use (removed)
- [x] redo as OOP
- [x] support generation without a max number given
- [x] do something with `arg` when generating all the possibilities
- [x] add a *changelog*
- [x] change comments symbols from `;` to `//` to more closely resemble *Chatito* v2.1.x
- [x] parser support *Chatito* v2.1.x's syntax for asking training and testing generations
- [x] as *Chatito* v2.1.x does, generate a testing dataset if asked
- [x] don't generate twice the same sentence
- [x] check that `casegen` is applicable and useful before setting it for a rule content
- [x] add the new training and testing syntax into the syntax specifications
- [x] *Docs* deprecate semi-colong syntax
- [x] *Docs* add warning about circular references
- [x] tie the "all possibilities" generation to a maximum
- [x] training and testing datasets should never overlap
- [x] support `arg` inside synonym lists
- [x] `generate_random` and `generate_all` don't have coherent arguments
- [x] allow for (most) special characters without escapement outside of units
- [x] replace modifier regex by several ones to allow for escaping special characters everywhere
- [x] use symbols from `parser_utils` everywhere needed
- [x] improve the overall command line experience (with `argparse`)
- [x] change `main.py` to a more user-friendly name
- [x] accept `train` AND `training` for training set number of intents
- [x] add a seed for random number generation
- [x] add a program argument for setting the seed
- [x] set output file path with respect to current working directory rather than input file directory
- [x] add a `--version` program argument
- [x] use python's built-in `DeprecationWarning` rather (print a warning for deprecations)
- [x] *Docs* make a wiki rather than a markdown file
- [x] add interactive mode (generate what the user asks through a CLI)
- [x] *Docs* explain '/' syntax for alternative slot value
- [x] wipe the output directory before writing new files
- [x] *Interactive mode*: add support for variations in relevant commands
- [x] *Interactive mode*: show list of variation names in command `show`
- [x] check for circular includes
- [x] use more list/dict comprehensions (faster than using `append`)

# Bugs

- **BUG**: arguments are not given down when an argument is transmitted as the argument of a token
- **BUG**: random generation modifiers' names are not taken into account when generating all examples
- **BUG**: a leading space is generated even though a unit has a random gen modifier and the unit wasn't generated
- **BUG**: it seems that `generate_all` of choice is called before the generation starts
- **BUG**: `{my [own?]/a} ~[religion]` can generate a double space
- **BUG**: space at the end of lines in json outputs

## To confirm
- Some intents don't generate any string even though they should

## Fixed bugs

- **fixed**: no case changing when asked with uppercase feeding
- **fixed**: escapment not currently working
- **fixed**: slots starting with a word crash the script
- **fixed**: can't parse when a content line is commented out
- **fixed**: sometimes the adapter can't find the text entity inside the example
- **fixed**: choice flattens its rules
- **fixed**: double spaces sometimes
- **fixed**: comment lines inside definitions aren't truly ignored
- **fixed**: fix bug with ']' generated in word groups within choices (`{[test ~[this]]/[and ~[this]]}`)
- **fixed**: some slot values are not present in the synonym list even if they have synonyms
- **fixed**: when changing case, some entities cannot be found any longer
- **fixed**: when no DummySlotValRuleContent, synonyms keep entities
- **fixed**: duplicates in synonym list
- **fixed**: in synonyms, too many synonyms are added because variations are not taken into account at generation
- **fixed**: entities are not generated with `generate_all`
- **fixed**: arguments are not correctly managed within entities list
- **fixed**: potential ImportErrors when running from `run.py` from the command line
- **fixed**: somewhere in the synonyms: Rasa NLU can't generate it without crashing (unhashable type 'dict' when looking for "value")
- **fixed**: `parser` exists as a basic Python module and is sometimes imported in place of the parser (renamed `parsing`)
- **fixed**: empty examples were duplicated on generation when trying to change their leading letter's case
- **fixed**: if a slot generated a certain string and this string could already be found somewhere before in the example, the first string was wrongly selected as the entity with the Rasa adapter
- **fixed**: indentation error raised for lines with only spaces
- **fixed**: when an empty alias definition is used, nothing is generated
- **fixed**: when using `save` command, variations print several times the same rule
- **fixed**: when using `save` command, `\$` are saved instead of `$`
- **fixed**: when using `save` command, choice are appended `?True`
- **fixed**: choices get a randgen when there is 1 `?` somewhere in their content
- **fixed**: several `?` in a choice's content crash the program (because of randgen)
- **fixed**: synonyms are synonyms of themselves (look at simple airport example)
- **fixed**: restaurant example doesn't seem to work anymore
- **fixed**: possible to have several times the same example generated
- **fixed**: encoding errors under Windows
- **fixed**: the interactive console seems to crash at `input()`?

# Ideas


## Rejected

- **rejected**: use overrides pip package (no, doesn't work in python 2)
- **rejected**: make arguments several layers deep? no, it is not useful as you can pass arguments down the references
- **rejected**: maybe add more modifiers to choices? no, rather merge it into word groups
