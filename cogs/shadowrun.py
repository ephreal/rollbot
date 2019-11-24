# -*- coding: utf-8 -*-

"""
Copyright 2018-2019 Ephreal

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import json
import aiohttp

from classes.roll_functions import roller
from classes.bot_utils import utils
from classes.context_handlers import shadowrun_handler as sh
from .cog_command_usage.helptext import shadowrun_help as sr_help

from discord.ext import commands
# from discord import client


class shadowrun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.handler = sh.ShadowrunHandler()
        self.roller = roller()
        self.utils = utils(self.bot)
        self.previous_rolls = []
        # I gotta admit... I chuckled a little writing down "self.help"
        self.help = sr_help()

        with open("config/config.json", 'r') as f:
            self.sr_tweaks = json.load(f)["sr_tweaks"]

    @commands.command(description="Shadowrun dice roller")
    async def sr(self, ctx):
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

        author = ctx.message.author.name
        author = author.split("#")[0]

        message = f"```Please try again {author}, I'm not sure what to do "\
                  "with that."

        command = ctx.message.content.lower().split()
        command = command[1:]

        channel = await self.utils.check_roll_channel(ctx)

        if len(command) == 0:
            return await channel.send("please run '.help sr' or .sr help for"
                                      " examples.")
        message = f"```CSS\nRan by {author}\n"

        if command[0].startswith("ro"):
            message += await self.roll(author, command[1:])
        elif command[0].startswith("i"):
            message += await self.roll_initiative(command[1:])
        elif command[0].startswith("h"):
            message += await self.sr_help(command[1:])
        elif command[0].startswith("e"):
            message += await self.extended(command[1:])
        elif command[0].startswith("q"):
            message += await self.quote(command[1:])

        message += "```"

        await channel.send(message)

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

        dice_pool = int(commands[0])
        threshold = int(commands[1])

        extended_test = self.handler.extended_test(dice_pool, threshold, prime)
        extended_test = await extended_test
        extended_test = self.handler.format_extended_test(extended_test)
        extended_test = await extended_test

        return extended_test

    async def roll_initiative(self, commands):
        """
        Rolls initiative. Shadowrun 1E requries a dice pool and reaction.
        Shadowrun 5E requires a dice pool and a modifier.
        """

        commands, prime = await self.check_prime(commands)

        try:
            dice_pool = int(commands[0])
            modifier = int(commands[0])

            initiative = self.handler.roll_initiative(dice_pool, modifier)
            initiative = await initiative

            initiative = await self.handler.format_initiative(initiative)

            return initiative

        except ValueError:
            return "Invalid input. Please give two numbers indicating dice "\
                   "and modifications.\nie: .sr initiative <dp> <mod>\n"\
                   "example: .sr initiative 5 3\n"\
                   "For more help, run .sr help initiative."

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

        if self.handler.edition == 1:
            threshold = commands[1]
            roll = await self.handler.roll(dice_pool)
            checked = await self.handler.check_roll(roll, threshold=threshold)

        elif self.handler.edition == 5:
            commands, exploding = await self.check_exploding(commands)
            roll = await self.handler.roll(dice_pool, exploding=exploding)
            checked = await self.handler.check_roll(roll, prime=prime)

        return await self.handler.format_roll(roll, checked, verbose=verbose)

    async def quote(self, quote_type):

        url = "https://shadowrun.needs.management/api.php?"
        bbcode_tags = [
                        "[b]", "[/b]", "[i]", "[/i]",
                        "[u]", "[/u]", "[s]", "[/s]"
                      ]

        html_escaped = {
                          "&quot;": '"',
                          "&amp;":  "&"
                        }

        try:
            if not quote_type:
                url += "random=true"
            elif quote_type[0] == "random":
                url += "random=true"
            elif quote_type[0] == "latest":
                url += "latest=true"
            elif int(quote_type[0]):
                url += f"quote_id={quote_type[0]}"
            else:
                url += "random=true"

        except Exception:
            url += "random=true"

        finally:

            async with aiohttp.ClientSession(
                  connector=aiohttp.TCPConnector(verify_ssl=True)) as session:

                html = await self.fetch(session, url)
                html = json.loads(html)
                return_string = f"quote id:     {html['id']}\n"
                return_string += f"written:      {html['time']}\n"
                return_string += f"quote author: {html['author']}\n\n"
                return_string += f"quote title:  {html['title']}\n"
                return_string += f"{html['quote']}"

            for i in bbcode_tags:
                return_string = return_string.replace(i, "")

            for i in html_escaped.keys():
                return_string = return_string.replace(i, html_escaped[i])

            if "[ul]" in return_string:
                return_string = return_string.replace("[ul]", "")
                return_string = return_string.replace("[/ul]", "")
                return_string = return_string.replace("[*]", "*")

            elif "[ol]" in return_string:
                count = 1
                return_string = return_string.replace("[ol]", "")
                return_string = return_string.replace("[/ol]", "")

                amount = return_string.count("[*]")

                for _ in range(0, amount):
                    current = return_string.find("[*]")
                    start = return_string[0:current]
                    end = return_string[current+3:]
                    return_string = f"{start}{count}) {end}"
                    print(return_string)
                    count += 1

        return return_string

    async def fetch(self, session, url):
        async with session.get(url) as html:
            return await html.text()


def setup(bot):
    bot.add_cog(shadowrun(bot))
