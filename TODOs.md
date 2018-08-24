# TODOs

- TODO: remake as OOP
- TODO: add argument support
- TODO: make arguments several layers deep?
- TODO: don't generate twice the same sentence
- TODO: generate all possible sentences when asked (tied to a maximum)
- TODO: add casegen inside declarations
- TODO: replace modifier regex by several one to allow for escaping special characters everywhere
- **TODO**: add choice support in OOP rewriting

## Done

- done: fix line number count for different files
- done: add unicode support for all files (io.open autodetects encoding i think)
- **done**: fix overriding of rules
- **done**: add entities when generating slot in OOP rewriting

# Bugs

- BUG: There seems to be a bug with choices not appearing even when they have to (rarely happens)
- fixed?: Fix bug with ']' generated in some rules
- BUG: can't parse when a content line is commented out

## Fixed bugs

- fixed: No case changing when asked with uppercase feeding
- fixed: escapment not currently working
- fixed: slots starting with a word crash the script
