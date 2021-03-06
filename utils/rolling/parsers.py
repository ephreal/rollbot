# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import argparse


class InvalidArgumentsError(Exception):
    """Raise an InvalidArgumentsError instead of exiting the program"""
    pass


class BaseRollParser(argparse.ArgumentParser):
    """
    Base roll handler to be extended
    """
    def __init__(self):
        super().__init__()
        self.prog = "BaseRoller"
        self.add_argument('dice', metavar="XdY", default="", nargs="?",
                          help="dice, in XdY format")
        self.add_argument('-n', '--note', nargs="*",
                          help="Note about this roll")

    def error(self, message):
        raise InvalidArgumentsError


class BasicRollParser(BaseRollParser):
    """
    Handles basic roll parsing.
    """
    def __init__(self):
        super().__init__()
        self.prog = "BasicRoller"
        self.add_argument('mod', type=int, default=0, nargs="?",
                          help="modifier to add to final result")


class DndRollParser(BasicRollParser):
    def __init__(self):
        super().__init__()
        self.prog = "DnDRoller"
        group = self.add_mutually_exclusive_group()
        group.add_argument("-adv", action="store_true")
        group.add_argument("-dis", action="store_true")


class Sr3RollParser(BaseRollParser):
    """
    A roll parser for shadowrun.
    """

    def __init__(self):
        super().__init__()
        self.prog = "Sr3Roller"
        self.add_argument("threshold", default=4, nargs="?", type=int,
                          help="The threshold the roll must meet or exceed")
        self.add_argument('-m', "--mod", type=int, default=0,
                          help="modifier to add to final result")
        self.add_argument("-i", "--initiative", "--init", default=0, nargs="?",
                          type=int, help="Initiative score to add to roll")
        self.add_argument("-o", "--open", action="store_true",
                          help="Gets open ended test threshold")


class Sr5RollParser(BaseRollParser):
    """
    A roll parser for shadowrun.
    """

    def __init__(self):
        super().__init__()
        self.add_argument('-ext', '--extended', action='store_true')


class VampireMasqueradeParser(BaseRollParser):
    def __init__(self):
        super().__init__()
        self.prog = "VM Roller"
        self.add_argument("difficulty", default=6, nargs="?", type=int,
                          help="The threshold the roll must meet or exceed")
        self.add_argument("mod", default=0, nargs="?", type=int,
                          help="Not really used im vampire the masquerade")
