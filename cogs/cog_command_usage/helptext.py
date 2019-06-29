"""
Some commands use the command input to call a different command. This is where
the help text for those subcommands is store. Were it not for this, the
help text for the base command (ie: ".sr") would be too long to be displayed
on discord.
"""

# Shadowrun commands help


class shadowrun_help():
    def __init__(self):

        self.SR_GENERAL_USE = \
            """
Help for sr commands.

.sr help gives you additional help for all .sr
commands. Available sr commands are

help (h)
extended (e)
initiative (i)
roll (r)

To use it, simply run
.sr help <command>

Examples:
    Get help for the roll command
    .sr help roll
    .sr help r
"""

        self.SR_EXTENDED = \
            """
Shadowrun extended test rolling

.sr extended allows rolling for extended tests.

Give it the dice pool to roll with, and the threshold to try meet, and it will
roll until the hits either meet/pass the threshold, or until the dice run out.

If the commands are configured to fail when a glitch or critical glitch occur,
the extended test will fail and let you know if a normal/critical glitch
occured.

Critical glitches fail the exteded test by default. This can be changed in the
config file.

Examples:
    run an extended test with a pice pool of 10 and
    a threshold of 5
    .sr extended 10 5
    .sr e 10 5

    Extended test. Dice pool 20, threshold 10
    .sr extended 20 10
    .sr e 20 10
"""

        self.SR_INITIATIVE = \
            """
Shadowrun initiative rolling

.sr initiative allows rolling for initiative and automatically adds in any
modifiers.

When rolling initiative, the first number is the amount of dice to roll (up
to 5 as per shadowrun 5E rules), and the second number is the modifier.

Like most sr commands, this command can be shortened to just "i".

.sr i <dice> <modifier>

Examples:
    roll 4 dice, add 10 to the result
    .sr initiative 4 10

    roll 5 dice, add 10 to the result
    .sr i 5 10
"""

        self.SR_ROLL = \
            """
Shadowrun dice rolling.

.sr roll allows you to roll dice using the rules for Shadowrun. This includes
automatically counting hits, misses, and ones. In addition, the command
accepts various flags to modify how hits, misses, ones, and glitches are
handled.

The roll command can be shortened to just "r" for convenience.

Accepted flags: prime, show

Examples:
    roll 10 dice. Counts hits, checks for glitches.
    .sr roll 10
    .sr r 10

    roll 10 dice, count 4's as a hit (prime runner quality)
    .sr roll 10 prime

    roll 10 dice, show the result of all rolls
    .sr roll 10 show

    roll 10 dice, count 4's as hits. Show all rolls.
    .sr roll 10 show prime
    .sr r prime show 10
"""
