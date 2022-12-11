# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import json

from discord.ext import commands
from utils import message_builder
from utils.rolling import rolling_utils
from utils.handlers import shadowrun_handler as sh
from utils import shadowrun_utils
from .cog_command_usage.helptext import shadowrun_help as sr_help


class shadowrun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.handler = sh.ShadowrunHandler()
        self.previous_rolls = []
        # I gotta admit... I chuckled a little writing down "self.help"
        self.help = sr_help()

        with open("config/config.json", 'r') as f:
            self.sr_tweaks = json.load(f)["sr_tweaks"]

    @commands.command(description="Shadowrun dice roller")
    async def sr(self, ctx, *roll_args):
        """
        Shadowrun specific dice rolling.

        The sr command is used for anything related to
        shadowrun. It has five subcommands: extended, initiative, quote,
        roll, and reroll. Extended rolls SR extended tests, initative rolls
        SR initative, quote gets a shadowrun quote from my quotesite, roll
        does dice rolling, and reroll allows rerolling the last roll you did.

        examples:
            roll:
                roll 10 dice
                .sr roll 10
                .sr r 10

            initiative:
                roll 3 dice, add 8 to the result
                .sr initiative 3 8
                .sr i 3 8

            extended:
                roll an extended test with a dicepool of 20
                and a threshold of 5.
                .sr extended 20 5
                .sr e 20 5

            quote:
                get a random shadowrun quote
                .sr quote

            reroll:
                roll previous dice roll
                .sr reroll

        For more in depth help, please run .sr help <command>

        This command is currently unfinished. More features
        are planned on being added in the future.
        """

        channel = ctx.channel

        if self.bot.restrict_rolling:
            channel = await rolling_utils.check_roll_channel(ctx, self.bot)

        roll_args = list(roll_args)

        message = ""

        if len(roll_args) == 0:
            message += await self.extended(roll_args[1:])
        elif roll_args[0].startswith("e"):
            message += await self.extended(roll_args[1:])
        elif roll_args[0].startswith("h"):
            message += await self.sr_help(roll_args[1:])
        elif roll_args[0].startswith("i"):
            message += await self.roll_initiative(roll_args[1:])
        elif roll_args[0].startswith("q"):
            quote = await self.quote(roll_args[0:])
            return await ctx.send(embed=quote)
        elif roll_args[0].startswith("re"):
            message += await self.reroll(ctx, roll_args[1:])
        elif roll_args[0].startswith("ro"):
            message += await self.roll(ctx.author, roll_args[1:])
        elif roll_args[0].startswith("v"):
            message += await self.set_version(roll_args[1:])

        message = await message_builder.embed_reply(ctx.author, message)

        _, gm_roll = await self.check_gm_roll(roll_args[1:])

        if gm_roll:
            await ctx.message.delete()
            return await ctx.author.send(message)

        await channel.send(embed=message)

    async def check_exploding(self, commands):
        """
        Checks shadowrun 5E commands to see if the dice are supposed to be
        re-rolled on 6's.
        """

        exploding = False
        exploding_commands = ["explode", "-ex", "edge", "-edge"]

        for i in exploding_commands:
            if i in commands:
                exploding = True
                commands.pop(commands.index(i))

        return commands, exploding

    async def check_gm_roll(self, commands):
        """
        Checks to see if the roll is a gm roll to be seen only in secret.
        """

        gm_roll = False
        gm_commands = ["gm", "-gm", "secret"]

        for i in gm_commands:
            if i in commands:
                gm_roll = True
                commands.pop(commands.index(i))

        return commands, gm_roll

    async def check_prime(self, commands):
        """
        Checks to see if 'prime' is in the commands list.

        commands: list[str]

            -> commands: list[str], prime: boolean
        """

        prime = False
        prime_commands = ['prime', '-p', 'primer']

        for i in prime_commands:
            if i in commands:
                commands.pop(commands.index(i))
                prime = True

        return commands, prime

    async def check_verbose(self, commands):
        """
        Checks to see if a command is supposed to be verbose.
        commands: list[str]

            -> commands: list[str], verbose: bool
        """

        verbose = False
        verbose_commands = ['show', 'verbose', '-v']

        for i in verbose_commands:
            if i in commands:
                verbose = True
                commands.pop(commands.index(i))

        return commands, verbose

    async def extended(self, commands):
        """
        Gives the context handler the required information to run an extended
        test. See classes.dice_rolling.shadowrun_rolling.py for more
        information.
        """

        if len(commands) < 2 or (len(commands) < 3 and 'prime' in commands):
            return "I need more information to run an extended test.\n"\
                   "Please give me both a dice pool and a threshold.\n"\
                   "ex: .sr extended 5 10\n"\
                   "run\n.sr help extended\nfor more help."

        commands, prime = await self.check_prime(commands)
        commands, _ = await self.check_verbose(commands)
        commands, exploding = await self.check_exploding(commands)

        dice_pool = int(commands[0])
        threshold = int(commands[1])

        extended_test = self.handler.extended_test(dice_pool, threshold, prime,
                                                   exploding)
        extended_test = await extended_test
        extended_test = self.handler.format_extended_test(extended_test)
        extended_test = await extended_test

        return extended_test

    async def roll_initiative(self, commands):
        """
        Rolls initiative. Shadowrun 1E requries a dice pool and reaction.
        Shadowrun 5E requires a dice pool and a modifier.
        """

        commands, _ = await self.check_prime(commands)
        commands, verbose = await self.check_verbose(commands)

        try:
            dice_pool = int(commands[0])
            modifier = int(commands[0])

            initiative = self.handler.roll_initiative(dice_pool, modifier)
            roll, initiative = await initiative

            initiative = await self.handler.format_initiative(roll, initiative,
                                                              verbose=verbose)

            return initiative

        except ValueError:
            return "Invalid input. Please give two numbers indicating dice "\
                   "and modifications.\nie: .sr initiative <dp> <mod>\n"\
                   "example:  .sr initiative 5 3\n"\
                   "For more help, run .sr help initiative."

    async def reroll(self, ctx, commands):
        """
        Rerolls a past roll (specific to SR5E).

        author: str
        """

        author = ctx.author.name

        commands, prime = await self.check_prime(commands)
        commands, verbose = await self.check_verbose(commands)

        reroll = await self.handler.reroll(author, prime=prime)

        returned_text = f"original_roll: {reroll['old']['roll']}\n"
        glitch = await self.handler.sr5_is_glitch(reroll['reroll'],
                                                  reroll['checked']['hits'])
        returned_text += await self.handler.format_roll(reroll['reroll'],
                                                        reroll['checked'],
                                                        verbose=verbose,
                                                        glitch=glitch)

        return returned_text

    async def roll(self, author, commands):
        """
        Rolls dice for shadowrun. Each edition will return slightly different
        results.

        author: ctx.author
        commands: list[str]
        """

        if not commands:
            return "Please give a dice pool.\n"\
                   "For help, run '.sr help roll'"

        commands, prime = await self.check_prime(commands)
        commands, verbose = await self.check_verbose(commands)
        dice_pool = int(commands[0])
        glitch = None

        if self.handler.edition == 1:
            threshold = int(commands[1])
            roll = await self.handler.roll(dice_pool)
            checked = await self.handler.check_roll(roll, threshold=threshold)

        elif self.handler.edition == 5:
            commands, exploding = await self.check_exploding(commands)
            roll = await self.handler.roll(dice_pool, exploding=exploding)
            checked = await self.handler.check_roll(roll, prime=prime)
            glitch = await self.handler.sr5_is_glitch(roll, checked['hits'])

        await self.handler.add_roll(author, roll, checked)

        return await self.handler.format_roll(roll, checked, verbose=verbose,
                                              glitch=glitch)

    async def set_version(self, commands):
        """
        Sets the current shadowrun version.
        """

        try:
            version = int(commands[0])
            if version > 5 or version < 0:
                version = 5
            await self.handler.set_sr_edition(version)
            return f"Shadowrun edition set to {version}"
        except ValueError:
            return "Please try again. That is not a valid shadowrun edition."

    async def sr_help(self, command):
        """
        Additional help for sr commands.

        Added because the current help for sr is getting
        a bit too long. This allows getting info for a
        specific command without having to wade through
        a bunch of extraneous info.
        """

        if len(command) == 0:
            helptext = self.help.SR_GENERAL_USE

        elif command[0].startswith("e"):
            helptext = self.help.SR_EXTENDED

        elif command[0].startswith("i"):
            helptext = self.help.SR_INITIATIVE

        elif command[0].startswith('re'):
            helptext = self.help.SR_REROLL

        elif command[0].startswith("ro"):
            helptext = self.help.SR_ROLL

        elif command[0].startswith("q"):
            helptext = self.help.SR_QUOTE

        else:
            helptext = "Shadowrun command not found."

        return helptext

    async def quote(self, quote_type):
        """
        Fetches a shadowrun quote
        """

        if len(quote_type) == 1:
            quote_type = "random"
        else:
            quote_type = quote_type[1]

        quote = await shadowrun_utils.get_quote(quote_type)
        quote = await shadowrun_utils.remove_bbcode(quote)
        quote = await shadowrun_utils.replace_bbcode(quote)
        quote = await shadowrun_utils.replace_html_escapes(quote)
        return await shadowrun_utils.format_quote(quote)


async def setup(bot):
    await bot.add_cog(shadowrun(bot))
