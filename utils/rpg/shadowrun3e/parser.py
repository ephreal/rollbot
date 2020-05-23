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

subparsers = Sr3CharacterParser.add_subparsers()

roll_parser = subparsers.add_parser('roll', help="roll help")
roll_parser.add_argument("threshold", nargs="?", help="roll threshold")
roll_group = roll_parser.add_mutually_exclusive_group()
roll_group.add_argument("-a", "--attribute", nargs="?", help="roll attribute")
roll_group.add_argument("-sk", "--skill", nargs="?", help="roll skill")
roll_group.add_argument('-sp', '--spell', nargs="?", help='roll spell')
roll_parser.add_argument("-n", "--note", nargs="*")

# Defining a subparser 'r' to make rolling more convenient. Exactly the same
# as the parser above. There's GOTTA be a better way to do this, but I don't
# know it yet.
r_parser = subparsers.add_parser('roll', help="roll help")
r_parser.add_argument("threshold", nargs="?", help="roll threshold")
r_group = r_parser.add_mutually_exclusive_group()
r_group.add_argument("-a", "--attribute", nargs="?", help="roll attribute")
r_group.add_argument("-sk", "--skill", nargs="?", help="roll skill")
r_group.add_argument('-sp', '--spell', nargs="?", help='roll spell')
r_parser.add_argument("-n", "--note", nargs="*")

skill_parser = subparsers.add_parser("skill", help="View and modify skills")
skill_parser.add_argument("skill", nargs="?", help="skill to view or modify")
skill_group = skill_parser.add_mutually_exclusive_group()
skill_group.add_argument("-a", "--add", action="store_true",
                         help="Add a skill")
skill_group.add_argument("-s", "--set", help="Set a skill to a value")
skill_group.add_argument("-m", "--modify", help="modify a skill")

spell_parser = subparsers.add_parser("spell", help="View/add/remove spells")
spell_parser.add_argument("spell", nargs="?", help="Spell to view or modify")
spell_group = spell_parser.add_mutually_exclusive_group()
spell_group.add_argument("-a", "--add", action="store_true",
                         help="Add a spell")
spell_group.add_argument("-r", "--remove", action="store_true",
                         help="remove a spell")

# Again... there's GOTTA be a better way....
attr_parser = subparsers.add_parser("attribute", help="view/modify attributes")
attr_parser.add_argument("attribute", nargs="?", help="attribute to view")
attr_parser.add_argument("-m", "--modify", help="modify an attribute")
attr_parser.add_argument("-o", "--override", help="override an attribute")

attr = subparsers.add_parser("attr", help="view/modify attributes")
attr.add_argument("attribute", nargs="?", help="attribute to view")
attr.add_argument("-m", "--modify", help="modify an attribute")
attr.add_argument("-o", "--override", help="override an attribute")

a_parser = subparsers.add_parser("a", help="view/modify attributes")
a_parser.add_argument("attribute", nargs="?", help="attribute to view")
a_parser.add_argument("-m", "--modify", help="modify an attribute")
a_parser.add_argument("-o", "--override", help="override an attribute")
