# TODOs

- [ ] parse in a better way asked number of generation of intents
- [ ] accept `#` as intent symbol (as well as `%` currently) to get closer to IBM Watson's syntax
- [ ] add some kind of optional version number within template files

- [ ] add an adapter to output raw lists of questions (rather than a JSON file)

- [ ] add opposite `randgen` names
- [ ] support several arguments in one rule
- [ ] reverse regex
- [ ] add probabilities of generation for rules in defintions (cf. https://github.com/rodrigopivi/Chatito/issues/48)
- [ ] add support Chatito's augmentations (cf. https://github.com/rodrigopivi/Chatito/issues/48)
- [ ] add a flag to enable/disable the slot = slot synonym behavior (cf. https://github.com/rodrigopivi/Chatito/issues/50)
- [ ] add a way to make some generation mandatory in the training set, test set or both (cf. https://github.com/rodrigopivi/Chatito/issues/51)
- [ ] add custom annotations as *Chatito* does

- [ ] add regex to rasa JSON file

- [ ] add a command line argument to specifiy the max number of examples to generate
- [ ] add bulk generation
- [ ] add interactive mode (generate what the user asks through a CLI)

- [ ] use more list/dict comprehensions (faster than using `append`)
- [ ] design patterns
- [ ] improve logging (remove `print`s and use a logging library)
<!-- - [ ] rewrite docstrings formatted as explained in *PEP257* -->
- [ ] check for circular includes
- [ ] detect and warn about circular references
- [ ] warn if there are slots within slots
- [ ] warn if the limit of examples generated was reached

- [ ] complete refactor of the code: the code is almost unmaintainable
- [ ] refactor units to remove duplicated code
- [ ] add more unit tests

- [ ] *Docs* add a representation of the architecture of the project
- [ ] *Docs* multilingual
- [ ] *Docs* make a wiki rather than a markdown file
- [ ] *Docs* specify which version of *Rasa NLU* *chatette* can work with

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
- [X] use python's built-in `DeprecationWarning` rather (print a warning for deprecations)

# Bugs

- **BUG**: arguments are not given down when an argument is transmitted as the argument of a token
- **BUG**: wrong generation when putting an alias inside a word group
- **BUG**: encoding errors under Windows

## To confirm

- **BUG?**: restaurant example doesn't seem to work anymore

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

# Ideas

- **IDEA**: maybe add more modifiers to choices?

## Rejected

- **rejected**: use overrides pip package (no, doesn't work in python 2)
- **rejected**: make arguments several layers deep? no, it is not useful as you can pass arguments down the references
