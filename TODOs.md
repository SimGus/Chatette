# TODOs

- TODO: add argument support
- TODO: don't generate twice the same sentence
- TODO: generate all possible sentences when asked (tied to a maximum)
- TODO: add casegen inside declarations
- TODO: replace modifier regex by several one to allow for escaping special characters everywhere

## Done

- done: fix line number count for different files
- done: add unicode support for all files (io.open autodetects encoding i think)

# Bugs

- BUG: There seems to be a bug with choices not appearing even when they have to (rarely happens)
- fixed?: Fix bug with ']' generated in some rules

## Fixed bugs

- fixed: No case changing when asked with uppercase feeding
- fixed: escapment not currently working
- fixed: slots starting with a word crash the script
