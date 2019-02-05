# Command Line Interface
*This is currently a work in progress: this is not currently usable.*

Eventually, it will be possible to use *Chatette* in a dynamic way.

To do this, first, we execute *Chatette* in interactive mode:
```bash
python -m chatette -i <path-to-template-file>
```
or
```bash
python -m chatette --interactive <path-to-template-file>
```

In this mode, no output will be generated.

The program parses the template file(s) and we get to a command prompt:
```
[DBG] Parsing <path-to-template-file>
[DBG] Parsed!
Executing chatette in interactive mode.
What do you need?
>>>
```

It is possible that arrow keys don't work in this prompt depending on which terminal emulator you use.

## Commands
There, several commands can be ran.

- `stats` will display statistics about the parsed file(s), namely the number of defined units, aliases, slots and intents.

- `parse <file-path>` will parse the file at `<file-path>` (relatively to the master template file).

- `exist alias "<alias-name>"` will ask the program if an alias named `<alias-name>` was parsed. The program will give information about the alias (namely its name, modifiers and number of rules) if it does and say it doesn't exist otherwise. The same kind of commands exist for slots and intents: `exist slot "<slot-name>"` and `exist intent "<intent-name>"`.

- `show alias "<alias-name>"` will ask to show the rules that define alias `<alias-name>`. If it doesn't exist, an error is printed. The same thing exists for slots and intents: `show slot "<slot-name>"` and `show intent "<intent-name>"`.

- `rename alias "<alias-name>" "<new-alias-name>"` will change the name of alias `<alias-name>` to `<new-alias-name>`. Similar commands exist for slots and intents.

- `delete alias "<alias-name>"` will completely remove the alias `<alias-name>` from the parser's memory (as if it hadn't been in the parsed template file(s)). The same thing can be done for slots and intents.

- `hide alias "<alias-name>"` will temorarily remove the alias `<alias-name>` from the parser's memory. `unhide alias "<alias-name>"` restores this alias definition (and can be executed after any other unit have been hidden). The same thing can be done for slots and intents.

- `examples alias "<alias-name>"` will ask for all the possible strings generated when referring to alias `<alias-name>`. `examples slot "<slot-name>"` and `examples intent "<intent-name>"` exist as well. An error is printed if the alias/slot/intent doesn't exist. Variations can also be selected by appending `#<variation-name>` to the name of the unit.
   
   If we add a number at the end of one of those commands (separated from the command by a whitespace), we ask to limit the answer to X strings (selected randomly from the possible strings). If X is larger than the number of possible strings, the command simply returns all the possible strings.
   
- `generate <adapter> alias "<alias-name>"` generates all possible strings and formats them as they would if adapter `<adapter>` was used. Similar commands for slots and intents exist. Again, appending a number at the end of the command limits the number of examples generated.

  Two adapters currently exist: `rasa` and `jsonl`.
  
  `generate` alone will execute the generation as it would have executed in non-interactive mode. Adding the adapter's name will make this generation use this adapter.

- `declare alias "<alias-name>"` creates a new alias named `<alias-name>` in the parser. It will have no rules and no modifiers. Similar commands exist for slots and intents.

- `add-rule alias "<alias-name>" "<rule>"` adds a rule to the definition of an alias named `<alias-name>` (if it exists). Similar commands exist for slots and intents.

- `set-modifier alias "<alias-name>" <modifier-name> "<value>"` changes the value of the modifier `<modifier-name>` of the alias `<alias-name>`. Similar commands exist for slots and intents. Since those are unit declarations, the only modifiers they accept are "case generation" (`"True"` or `"False"` (case-insensitive)) and "argument identifier" (any string). Modifier names are thus `casegen` and `arg`.

  Beware that you could get exceptions later on if you set modifiers to invalid or incoherent values.
   
- `rule "<rule>"` will generate the rule using all the units that have been defined in the template file(s). We can redirect its outputs to a file as before. If you need to use double quotes in the rule, escape it with a backslash `\`.

- `save <file-path>` will create (or truncate) a file at `<file-path>` and save the configuration of the parser as templates. You will then be able to use this file as a template file later on with all the units you declared and modified during the interactive session.

- `execute "<path-to-file>"` will read the file `<path-to-file>` and execute all the commands that are inside it sequentially. The commands and results will be printed on the command line as those executions are made. The commands in the file should be separated by newlines (thus, one command per line). Lines starting with `//` are ignored.

  Chatette can also directly read the commands from this file by calling the script with:
  ```bash
  python -m chatette <path-to-template-file> -I <path-to-command-file>
  ```
  or
  ```bash
  python -m chatette <path-to-template-file> --interactive-commands-file <path-to-command-file>
  ```

  The interactive mode is entered after all the commands in the file have been executed,
  unless an `exit` command is found (the script is stopped immediately).

  The option `-i` or `--interactive` may be added, but will result in the same behavior.
  
- `exit` or `Ctrl+D` (`EOF`) stops the interactive mode (and the script). `Ctrl+C` would work as well, but stops *Chatette* abruptly without any exit message.

For all those commands (except `exit`), appending `> <filename>` or `>> <filename>` will respectively write the results into a file named `<filename>` (creating the file if it doesn't exist, overwriting it if it does) or append the results into a file named `<filename>` (creating it if it doesn't exist).

#### Current advancement
- [x] stats
- [x] parse
- [x] exist
- [x] show
- [x] rename
- [x] delete
- [x] hide
- [x] unhide
- [x] examples
- [x] generate
- [x] declare
- [x] add-rule
- [x] set-modifier
- [x] rule
- [x] save
- [x] execute
- [x] exit

### Regexes
Rather than using `<alias-name>` for the name of the alias (resp. any unit), you can use regexes in all those commands, in the following way `/regex/flag` where `regex` is the regex (defined as it should be to work with `re` in Python) and `flag` can be one of the following:

- `i`: the regex is case-insensitive
- `g`: the search looks for all matches and not just the first one

The command executed will then be run against all the units whose name contain at least one match.

