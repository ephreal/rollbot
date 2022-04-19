# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import argparse
import os


class InvalidArgumentsError(Exception):
    """Raise an InvalidArgumentsError instead of exiting the program"""
    pass


class BbsParser(argparse.ArgumentParser):

    def __init__(self):
        super().__init__()
        self.commands = self.get_commands()
        self.add_argument("command", nargs=1, help="Command to run")
        self.add_argument("parameters", nargs="*")

    def error(self, message):
        raise InvalidArgumentsError

    def get_commands(self):
        commands = []
        for command in os.listdir("utils/shadowland/commands"):
            if command.endswith(".py"):
                commands.append(command[:-3])
        return commands

    def check_command(self, string):
        self.parse_args(string)
        print(f"commands: {self.command}")
        print(f"parameters: {self.parameters}")
