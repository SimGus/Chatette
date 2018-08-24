# TODOs

- TODO: remake as OOP
- TODO: add argument support
- TODO: don't generate twice the same sentence
- TODO: generate all possible sentences when asked (tied to a maximum)
- TODO: replace modifier regex by several one to allow for escaping special characters everywhere
- **TODO**: use symbols from parser_utils everywhere needed
- **TODO**: add support for synonyms in OOP rewriting
- **TODO**: Rewrite docstrings formatted as explained in *PEP257*
- **TODO**: use more list/dict comprehensions (faster than using `append`)
- **TODO**: check that slot value in slots content has any use

## Done

- done: fix line number count for different files
- done: add unicode support for all files (io.open autodetects encoding i think)
- **done**: fix overriding of rules
- **done**: add entities when generating slot in OOP rewriting
- **done**: add casegen inside declarations
- **done**: add choice support in OOP rewriting
- **done**: slot value should be the whole text and not only the first word if no value is given
- **done**: remove escapement in slot values
- **done**: add a 'choose' function utility
- **done**: give a default nb of indent for `printDBG` methods

# Bugs

- BUG: There seems to be a bug with choices not appearing even when they have to (rarely happens)
- fixed?: Fix bug with ']' generated in some rules
- BUG: can't parse when a content line is commented out

## Fixed bugs

- fixed: No case changing when asked with uppercase feeding
- fixed: escapment not currently working
- fixed: slots starting with a word crash the script
- **fixed**: choice flattens its rules
- **fixed**: double spaces sometimes
- **fixed**: Comment lines inside definitions aren't truly ignored

# Ideas

- **IDEA**: make arguments several layers deep?
- **IDEA**: maybe add more modifiers to choices?

## Rejected

- **rejected**: use overrides pip package (no, doesn't work in python 2)
