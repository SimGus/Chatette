# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Interactive mode, executable using `-i` or `--interactive` program argument, with commands that give information or change the state of the parser after it read template files
- Add program option `-I` or `--interactive-commands-file` to feed the script a file of commands that will be directly executed

### Changed
- Accept comment lines and empty lines inside unit definitions (not considered as a new rule)
- Move tokenizer out of parser, move all code that is related to parsing into directory `parsing` and rename file `parsing.py` back to `parser.py`. Parsing might behave differently than it used to.

### Fixed
- Possible infinite loop during generation (with a lot of bad luck)
<!--- Sometimes, duplicate examples when asking for less than half of all possible examples-->
- (Invisible) warnings because of invalid control sequences in the code and the tests

## [1.3.2] - 2019-01-21
### Added
- Wiki explaining the whole syntax of template files and the usage of the program
- Examples for the wiki
- Use a built-in `DeprecationWarning` for deprecation warnings (additionally to printing the warning on stdout)

### Fixed
- Possible exception caused by missing import
- Output directory (provided by the user with `-o` or `--output` flag) was ignored

## [1.3.1] - 2019-01-10
### Added
- Program argument `-v` or `--version` to display the version number of the module (a `__version__` attribute of the module itself is also now available)

### Fixed
- Missing requirements when installing the package from [PyPI](https://pypi.org/project/chatette)
- Casegen (i.e. change of case for examples) didn't apply for some definitions (notably when not asking for a specific number of examples to be generated)
- Version number displayed in help messages in terminal

## [1.3.0] - 2018-12-30
### Added
- Code of conduct and instructions for contributing
- Unit tests for some parts of the projects (automatically run by Travis CI)
- New adapter that outputs `.jsonl` files (choosing which adapter to use is done with the program argument `-a` or `--adapter`)

### Changed
- The number of examples to generate for training and testing does not need to be surrounded with single quotes anymore (but still can): `'training':'5'` is accepted as well as `test: 3`
- The output files cannot contain more than 10000 examples anymore
- The output files are now by default put in folders `output/train/` and `output/test/`
- Refactoring of some parts of the code
- Script is now referred to as `chatette` rather than `chatette.run` when executing from the command line

### Fixed
- Using an empty definition now raises an exception rather than removing all generated examples
- Having a line with only spaces doesn't crash the script anymore
- When writing output files in Rasa format, the entity highlighted could be located incorrectly in the example text (if an entity value was used twice for example)
- Possible duplicated examples when generating units with different letter case

## [1.2.3] - 2018-11-22
### Added
- Program argument (`-l` or `--local`) to make the working directory be the directory containing the template file

### Changed
- Working directory to be the directory from which the command is executed

### Fixed
- Missing import in a particular case
- Several error messages that used legacy variables
- `parser.py` changed to `parsing.py` to avoid some computers importing the default Python module named `parser`

## [1.2.2] - 2018-11-04
### Added
- Program argument (`-s` or `--seed`) that is used as the seed of the random number generator

### Fixed
- Restaurant example which still had tests within it

## [1.2.1] - 2018-10-22
### Changed
- Accept `train` and `test` as well as `training` and `testing` for the identifiers of the numbers of examples to generate

### Fixed
- Potential `ImportError`s when running script directly from the command line
- Logo display on PyPI

## [1.2.0] - 2018-09-19
### Added
- Contributors to README

### Changed
- Chatette is now a [project on PyPI](https://pypi.org/project/chatette) :D

## [1.1.5] - 2018-09-19
### Added
- Files to make the script a package and register it on [PyPI](https://pypi.org)

### Changed
- More pythonic project structure

### Fixed
- Generator's max number of example setter missing a parameter

## [1.1.4] - 2018-09-16
### Added
- Possibility to change some special characters from the code

### Changed
- Accept modifiers in any order

## [1.1.3] - 2018-09-13
### Changed
- In synonyms lists, replace argument identifiers with their previously encountered values (i.e. each value accross the whole templates)

## [1.1.2] - 2018-09-11
### Added
- Hard limit on the generation of intent example to avoid producing too large files (by default, not more then 20'000 examples per intent)

### Changed
- Manage arguments within generated entities
- Release number to follow SemVer 2.0.0

### Fixed
- When asking to generate lots of examples, entities were not listed

## [1.1.1] - 2018-09-11
### Added
- Warning about circular references in the documentation

### Changed
- Deprecate semi-colon syntax in documentation

## [1.1.0] - 2018-09-11
### Added
- Support for generation of non-overlapping training and testing datasets
- Parser support for *Chatito* v2.1.x's syntax for asking for intent generation (`('training': '5', 'testing': '3')`). *Old way is not deprecated!*

### Changed
- Discard duplicates in generated examples (for both training and test datasets)
- Discard inapplicable case generation modifiers (in most cases)

### Deprecated
- Semi-colon `;` syntax for comments (rather use double slash `//` syntax) to stick closer to *Chatito* v2.1.x

## [1.0.0] - 2018-09-08
### Added
- Changelog
- Logo
- Syntax documentation
- Add shebang in all files

### Changed
- Update README to be nice for users
- Update real-life data
- Generate all possible examples when no number of generation is given: *Chatette* is now a superset of *Chatito* v2.0.0
- Use more list and dict comprehensions

## [0.4.2] - 2018-08-25
### Changed
- Take variations and synonyms into account when generating all possibilities
- Slash `/` syntax in slot definitions now takes the identifier of the first token of the rule to avoid having the same behavior as the empty equal syntax
- Update real-life data

### Fixed
- Empty synonyms list
- Incorrect letter case within entities

## [0.4.1] - 2018-08-24
### Removed
- Generator methods now unused with new parser

### Fixed
- Crashing *Rasa* adapter

## [0.4.0] - 2018-08-24
### Added
- Generate all possible strings for each and every token
- Synonym support (in *Rasa NLU* format) in generator

### Changed
- Rewrite the whole parser in an Object-Oriented way (with support for everything that was supported before)
- Update real-life data

### Fixed
- Escapement for arguments being removed too soon

## [0.3.2] - 2018-08-20
### Fixed
- Comment lines and empty lines within definitions being considered as rules
- Several bugs when referencing without variations a token defined with some

## [0.3.1] - 2018-08-19
### Removed
- Lots of debugging prints

## [0.3.0] - 2018-08-19
### Added
- Argument support
- Real-life data
- Random generation to choices

### Changed
- Possibility to use a token without variation even though it was defined with it
- Simplify the parser
- Check that tokens are named

### Fixed
- Keep track of leading spaces with choices
- Escapement within choices
- Line feed `\n` inside parsed strings
- Assumption that words provided to the generator begin with a lowercase letter

## [0.2.0] - 2018-08-17
### Added
- Support for choices in the parser and the generator
- Easier way to have a slot value named as the string generated (i.e. using slash `/` syntax)

### Changed
- Named random generations now generate (or don't generate) together

## 0.1.0 - 2018-08-17
### Added
- MIT license file
- README file
- .gitignore file
- Draft of syntax description
- Utility functions
- Complete parser with support for words, word groups, aliases, slots and intents
- Support for slot value names
- Generator able to generate an output file in *Rasa NLU* format (without support for synonyms or regex features)

[Unreleased]: https://github.com/SimGus/Chatette/compare/v1.3.2...HEAD
[1.3.2]: https://github.com/SimGus/Chatette/compare/v1.3.1...v1.3.2
[1.3.1]: https://github.com/SimGus/Chatette/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/SimGus/Chatette/compare/v1.2.3...v1.3.0
[1.2.3]: https://github.com/SimGus/Chatette/compare/v1.2.2...v1.2.3
[1.2.2]: https://github.com/SimGus/Chatette/compare/v1.2.1...v1.2.2
[1.2.1]: https://github.com/SimGus/Chatette/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/SimGus/Chatette/compare/v1.1.5...v1.2.0
[1.1.5]: https://github.com/SimGus/Chatette/compare/v1.1.4...v1.1.5
[1.1.4]: https://github.com/SimGus/Chatette/compare/v1.1.3...v1.1.4
[1.1.3]: https://github.com/SimGus/Chatette/compare/v1.1.2...v1.1.3
[1.1.2]: https://github.com/SimGus/Chatette/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/SimGus/Chatette/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/SimGus/Chatette/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/SimGus/Chatette/compare/v0.4.2...v1.0.0
[0.4.2]: https://github.com/SimGus/Chatette/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/SimGus/Chatette/compare/v0.3.2...v0.4.1
[0.4.0]: https://github.com/SimGus/Chatette/compare/v0.3.2...v0.4.0
[0.3.2]: https://github.com/SimGus/Chatette/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/SimGus/Chatette/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/SimGus/Chatette/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/SimGus/Chatette/compare/v0.1.0...v0.2.0
