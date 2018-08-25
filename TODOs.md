# TODOs


_ **TODO**: support `arg` inside synonym lists
- **TODO**: add *casegen* inside declarations
- **TODO**: add regex to rasa JSON file

- **TODO**: don't generate twice the same sentence
- **TODO**: tie the "all possibilities" generation to a maximum
- **TODO**: do something with `arg` when generating all the possibilities
- **TODO**: support generation without a max number given

- **TODO**: replace modifier regex by several one to allow for escaping special characters everywhere
- **TODO**: make arguments several layers deep?

- **TODO**: add a *changelog*

- **TODO**: improve the overall command line experience (cf. `click` library)

- **TODO**: use symbols from parser_utils everywhere needed
- **TODO**: Rewrite docstrings formatted as explained in *PEP257*
- **TODO**: use more list/dict comprehensions (faster than using `append`)

## Done

- **done**: fix line number count for different files
- **done**: add unicode support for all files (`io.open` autodetects encoding i think)
- **done**: add argument support
- **done**: generate all possible sentences when asked
- **done**: add synonyms into the synonym object of rasa JSON file
- **done**: fix overriding of rules
- **done**: add entities when generating slot in OOP rewriting
- **done**: add casegen inside declarations
- **done**: add choice support in OOP rewriting
- **done**: slot value should be the whole text and not only the first word if no value is given
- **done**: remove escapement in slot values
- **done**: add a 'choose' function utility
- **done**: give a default nb of indent for `printDBG` methods
- **done**: add support for synonyms in OOP rewriting
- **done**: check that slot value in slots content has any use (removed)
- **done**: redo as OOP

# Bugs

- **BUG**: somewhere in the synonyms: Rasa NLU can't generate it without crashing (unhashable type 'dict' when looking for "value")
- **BUG**: in synonyms, too many synonyms are added because variations are not taken into account at generation

## To confirm

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

# Ideas

- **IDEA**: make arguments several layers deep?
- **IDEA**: maybe add more modifiers to choices?

## Rejected

- **rejected**: use overrides pip package (no, doesn't work in python 2)
