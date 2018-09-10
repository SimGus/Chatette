# TODOs

- **TODO**: tie the "all possibilities" generation to a maximum

- **TODO**: do something with `arg` when generating all the possibilities
- **TODO**: support `arg` inside synonym lists
- **TODO**: add opposite `randgen` names
- **TODO**: support several arguments in one rule

- **TODO**: add regex to rasa JSON file
- **TODO**: replace modifier regex by several one to allow for escaping special characters everywhere
- **TODO**: use symbols from `parser_utils` everywhere needed
- **TODO**: training and testing datasets should never overlap

- **TODO**: improve the overall command line experience (cf. `click` library)
- **TODO**: allow for arguments to the command line (output file*s* paths)
- **TODO**: change `main.py` to a more user-friendly name

- **TODO**: use more list/dict comprehensions (faster than using `append`)
- **TODO**: rewrite docstrings formatted as explained in *PEP257*

- **TODO**: add unit tests

- **TODO**: *Docs* add warning about circular references
- **TODO**: *Docs* deprecate semi-colong syntax

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
- **done**: add a *changelog*
- **done**: change comments symbols from `;` to `//` to more closely resemble *Chatito* v2.1.x
- **done**: parser support *Chatito* v2.1.x's syntax for asking training and testing generations
- **done**: as *Chatito* v2.1.x does, generate a testing dataset if asked
- **done**: don't generate twice the same sentence
- **done**: check that `casegen` is applicable and useful before setting it for a rule content
- **done**: add the new training and testing syntax into the syntax specifications

# Bugs

## To confirm

- **BUG?**: somewhere in the synonyms: Rasa NLU can't generate it without crashing (unhashable type 'dict' when looking for "value")

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

# Ideas

- **IDEA**: make arguments several layers deep?
- **IDEA**: maybe add more modifiers to choices?

## Rejected

- **rejected**: use overrides pip package (no, doesn't work in python 2)
- **rejected**: make arguments several layers deep? no, it is not useful as you can pass arguments down the references
