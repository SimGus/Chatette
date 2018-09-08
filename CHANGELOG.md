# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### [1.0] - 2018-09-08
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

## [0.4] - 2018-08-24
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

## [0.3] - 2018-08-19
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

## [0.2] - 2018-08-17
### Added
- Support for choices in the parser and the generator
- Easier way to have a slot value named as the string generated (i.e. using slash `/` syntax)

### Changed
- Named random generations now generate (or don't generate) together

## 0.1 - 2018-08-17
### Added
- MIT license file
- README file
- .gitignore file
- Draft of syntax description
- Utility functions
- Complete parser with support for words, word groups, aliases, slots and intents
- Support for slot value names
- Generator able to generate an output file in *Rasa NLU* format (without support for synonyms or regex features)

[Unreleased]: https://github.com/SimGus/Chatette/compare/v1.0.0...HEAD
[1.0]: https://github.com/SimGus/Chatette/compare/v0.4.2...v1.0
[0.4.2]: https://github.com/SimGus/Chatette/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/SimGus/Chatette/compare/v0.3.2...v0.4.1
[0.4]: https://github.com/SimGus/Chatette/compare/v0.3.2...v0.4
[0.3.2]: https://github.com/SimGus/Chatette/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/SimGus/Chatette/compare/v0.3...v0.3.1
[0.3]: https://github.com/SimGus/Chatette/compare/v0.2...v0.3
[0.2]: https://github.com/SimGus/Chatette/compare/v0.1...v0.2
