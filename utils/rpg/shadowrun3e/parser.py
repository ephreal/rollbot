# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


__all__ = ('Sr3CharacterParser')


import argparse

Sr3CharacterParser = argparse.ArgumentParser()
Sr3CharacterParser.add_argument("-n", "--note")

subparsers = Sr3CharacterParser.add_subparsers()

roll_parser = subparsers.add_parser('roll', help="roll help",
                                    aliases=["r", "ro"])
roll_parser.add_argument("threshold", nargs="?", help="roll threshold",)
roll_group = roll_parser.add_mutually_exclusive_group()
roll_group.add_argument("-a", "--attribute", nargs="?", help="roll attribute")
roll_group.add_argument("-sk", "--skill", nargs="?", help="roll skill")
roll_group.add_argument('-sp', '--spell', nargs="?", help='roll spell')
roll_parser.add_argument("-n", "--note", nargs="*")
roll_parser.add_argument("--command", default="roll", help=argparse.SUPPRESS)


skill_parser = subparsers.add_parser("skill", help="View and modify skills")
skill_parser.add_argument("skill", nargs="?", help="skill to view or modify")
skill_parser.add_argument("modify", nargs="?", help="value to modify by")
skill_group = skill_parser.add_mutually_exclusive_group()
skill_group.add_argument("-a", "--add", action="store_true",
                         help="Add a skill")
skill_group.add_argument("-s", "--set", help="Set a skill to a value")
skill_group.add_argument("-m", "--modifier", help="modify a skill",
                         action="store_true")
skill_parser.add_argument("-n", "--note", nargs="*")
skill_parser.add_argument("--command", default="skill", help=argparse.SUPPRESS)


spell_parser = subparsers.add_parser("spell", help="View/add/remove spells")
spell_parser.add_argument("spell", nargs="?", help="Spell to view or modify")
spell_group = spell_parser.add_mutually_exclusive_group()
spell_group.add_argument("-a", "--add", action="store_true",
                         help="Add a spell")
spell_group.add_argument("-r", "--remove", action="store_true",
                         help="remove a spell")
spell_parser.add_argument("-n", "--note", nargs="*")


attr_parser = subparsers.add_parser("attribute", help="view/modify attributes",
                                    aliases=['a', 'attr'])
attr_parser.add_argument("attribute", nargs="?", help="attribute to view")
attr_parser.add_argument("modify", nargs="?", help="modify the attribute")
attr_parser.add_argument("-m", "--modifier", action="store_true",
                         help="Set the attribute modifier")
attr_parser.add_argument("-o", "--override", help="override an attribute")
attr_parser.add_argument("-s", "--set", action="store_true",
                         help="set attribute to the value given")
attr_parser.add_argument("-n", "--note", nargs="*")
attr_parser.add_argument("--command", default="attribute",
                         help=argparse.SUPPRESS)

karma_parser = subparsers.add_parser("karma", help="Add or remove karma")
karma_parser.add_argument("karma", nargs="?", help="Karma to add/remove")
karma_parser.add_argument("-n", "--note", nargs="*")
karma_parser.add_argument("--command", default="karma", help=argparse.SUPPRESS)
