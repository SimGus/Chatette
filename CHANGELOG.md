# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.5] - 2018-09-19
### Added
- Files to make the script a package and register it on [PyPI](https://pypi.org/project/chatette)

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

[Unreleased]: https://github.com/SimGus/Chatette/compare/v1.1.5...HEAD
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
