# TODOs

- **TODO**: redo as OOP

- **TODO**: add *casegen* inside declarations
- **TODO**: add synonyms into the synonym object of rasa JSON file
- **TODO**: add regex to rasa JSON file

- **TODO**: generate all possible sentences when asked (tied to a maximum)
- **TODO**: don't generate twice the same sentence
- **TODO**: support generation without a max number given

- **TODO**: replace modifier regex by several one to allow for escaping special characters everywhere
- **TODO**: make arguments several layers deep?

- **TODO**: add a *changelog*

## Done

- **done**: fix line number count for different files
- **done**: add unicode support for all files (`io.open` autodetects encoding i think)
- **done**: add argument support

# Bugs

- **BUG**: Fix bug with ']' generated in word groups within choices (`{[test ~[this]]/[and ~[this]]}`)

## To confirm

- There seems to be a bug with choices not appearing even when they have to (rarely happens)

## Fixed bugs

- **fixed**: No case changing when asked with uppercase feeding
- **fixed**: escapment not currently working
- **fixed**: slots starting with a word crash the script
- **fixed**: can't parse when a content line is commented out
- **fixed**: Sometimes the adapter can't find the text entity inside the example
