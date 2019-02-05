#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys

from chatette import __version__
from chatette.facade import Facade
from chatette.cli.interpreter import CommandLineInterpreter


def main():
    # pylint: disable=bad-continuation
    argument_parser = argparse.ArgumentParser(
        description="Chatette v"+__version__+" -- " +
                    "Generates NLU datasets from template files",
        epilog="SimGus -- 2018 -- Released under MIT license",
        prog="Chatette",
        add_help=True)

    argument_parser.add_argument("input", type=str,
                                 help="Path to master template file")

    argument_parser.add_argument("-v", "--version", action="version",
                                 version="%(prog)s v"+__version__,
                                 help="Print the version number of the module")

    argument_parser.add_argument("-o", "--out", dest="output", required=False,
                                 type=str, default=None,
                                 help="Output directory path")
    argument_parser.add_argument("-l", "--local", dest="local", required=False,
                                 action="store_true", default=False,
                                 help="Change the base directory for output " +
                                      "files from the current working directory " +
                                      "to the directory containing the template " +
                                      "file")

    argument_parser.add_argument("-a", "--adapter", dest="adapter", required=False,
                                 type=str, default="rasa",
                                 help="Write adapter. Possible values: "+
                                      "['rasa', 'jsonl']")

    argument_parser.add_argument("-s", "--seed", dest="seed", required=False,
                                 type=str, default=None,
                                 help="Seed for the random generator " +
                                      "(any string without spaces will work)")
                                      
    argument_parser.add_argument("-i", "--interactive", dest="interactive_mode",
                                 required=False, action="store_true",
                                 default=False,
                                 help="Runs Chatette in interactive mode")
    argument_parser.add_argument("-I", "--interactive-commands-file",
                                 dest="interactive_commands_file",
                                 required=False, default=None, type=str,
                                 help="Path to a file containing interactive " +
                                      "mode commands that will be directly run")

    if len(sys.argv[1:]) == 0:
        argument_parser.print_help()
        argument_parser.exit()

    args = argument_parser.parse_args()

    facade = Facade.get_or_create_from_args(args)
    if not args.interactive_mode and args.interactive_commands_file is None:
        facade.run()
    else:
        cli = CommandLineInterpreter(facade, args.interactive_commands_file)
        cli.wait_for_input()


if __name__ == "__main__":
    main()
