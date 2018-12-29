# TODOs

- **TODO**: parse in a better way asked number of generation of intents
- **TODO**: accept `#` as intent symbol (as well as `%` currently) to get closer to IBM Watson's syntax

- **TODO**: add an adapter to output raw lists of questions (rather than a JSON file)

- **TODO**: add opposite `randgen` names
- **TODO**: support several arguments in one rule

- **TODO**: add regex to rasa JSON file

- **TODO**: allow for arguments to the command line (output file*s* paths, max generation per intent,...)
- **TODO**: add bulk generation

- **TODO**: use more list/dict comprehensions (faster than using `append`)
- **TODO**: improve logging (remove `print`s and use a logging library)
<!-- - **TODO**: rewrite docstrings formatted as explained in *PEP257* -->
- **TODO**: detect and warn about circular references
- **TODO**: check for circular includes
- **TODO**: warn if there are slots within slots
- **TODO**: warn when empty alias definitions are used

- **TODO**: big refactor
- **TODO**: refactor units to remove duplicated code
- **TODO**: add more unit tests

- **TODO**: *Docs* add a representation of the architecture of the project

## Done

- **done**: fix line number count for different files
- **done**: add unicode support for all files (`io.open` autodetects encoding i think)
- **done**: add argument support
- **done**: generate all possible sentences when asked
- **done**: add synonyms into the synonym object of rasa JSON file
- **done**: fix overriding of rules
- **done**: add entities when generating slot in OOP rewriting
- **done**: add *casegen* inside declarations
- **done**: add choice support in *OOP* rewriting
- **done**: slot value should be the whole text and not only the first word if no value is given
- **done**: remove escapement in slot values
- **done**: add a `choose` function utility
- **done**: give a default nb of indent for `printDBG` methods
- **done**: add support for synonyms in OOP rewriting
- **done**: check that slot value in slots content has any use (removed)
- **done**: redo as OOP
- **done**: support generation without a max number given
- **done**: do something with `arg` when generating all the possibilities
- **done**: add a *changelog*
- **done**: change comments symbols from `;` to `//` to more closely resemble *Chatito* v2.1.x
- **done**: parser support *Chatito* v2.1.x's syntax for asking training and testing generations
- **done**: as *Chatito* v2.1.x does, generate a testing dataset if asked
- **done**: don't generate twice the same sentence
- **done**: check that `casegen` is applicable and useful before setting it for a rule content
- **done**: add the new training and testing syntax into the syntax specifications
- **done**: *Docs* deprecate semi-colong syntax
- **done**: *Docs* add warning about circular references
- **done**: tie the "all possibilities" generation to a maximum
- **done**: training and testing datasets should never overlap
- **done**: support `arg` inside synonym lists
- **done**: `generate_random` and `generate_all` don't have coherent arguments
- **done**: allow for (most) special characters without escapement outside of units
- **done**: replace modifier regex by several ones to allow for escaping special characters everywhere
- **done**: use symbols from `parser_utils` everywhere needed
- **done**: improve the overall command line experience (with `argparse`)
- **done**: change `main.py` to a more user-friendly name
- **done**: accept `train` AND `training` for training set number of intents
- **done**: add a seed for random number generation
- **done**: add a program argument for setting the seed
- **done**: set output file path with respect to current working directory rather than input file directory

# Bugs

- **BUG**: arguments are not given down when an argument is transmitted as the argument of a token
- **BUG**: wrong generation when putting an alias inside a word group
- **BUG**: encoding errors under Windows
- **BUG**: when an empty alias definition is used, nothing is generated

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

# Ideas

- **IDEA**: maybe add more modifiers to choices?

## Rejected

- **rejected**: use overrides pip package (no, doesn't work in python 2)
- **rejected**: make arguments several layers deep? no, it is not useful as you can pass arguments down the references
