# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord import Colour
from discord.ext import commands
from utils import message_builder
from utils.rolling import rolling_utils
from utils.rolling import handlers


class roller(commands.Cog):
    def __init__(self, bot):
        self.handlers = {
                    "basic": handlers.BaseRollHandler(),
                    "sr3": handlers.Sr3RollHandler()
        }
        self.handler = handlers.BaseRollHandler()
        self.guild_handlers = {}
        self.db = bot.db_handler.guild_config
        self.bot = bot

    @commands.command(pass_context=True)
    async def roll(self, ctx, *roll_args):
        """Rolls dice

        Rolls XdY dice.

        By default, the dice roller rolls dice with the currently set game
        mode. This can be changed with the ".set" command, or by passing in
        the "-g" parameter.

        roll 10, six-sided dice
            .roll 10d6

        Add 5 to 10, six sided dice
            .roll 10d6 -m 5

        Give a note specifying what the note is for
            .roll 1d6 -n This is a test roll
        """

        try:
            handler = self.handlers[ctx.guild.id]
        except KeyError:
            handler = self.db.get_handler(ctx.guild.id)

        channel = await rolling_utils.check_roll_channel(ctx, self.bot)
        if "-h" in roll_args:
            message = self.handler.parser.format_help()
            message = f"```{message}```"
            return await ctx.send(message)

        roll = await self.handler.roll(roll_args)
        message = await roll.format()

        if "CRITICAL" in message or "FAILURE" in message:
            message = await message_builder.embed_reply(ctx.author, message,
                                                        Colour.red())
        else:
            message = await message_builder.embed_reply(ctx.author, message)

        await channel.send(embed=message)

    @commands.command(description="Sets current rolling mode")
    async def roll_config(self, ctx, mode):
        """Sets the current rolling mode.

        Valid options are "basic" and "sr3"
        """

        if mode == "basic":
            self.handler = handlers.BaseRollHandler()
        elif mode == "sr3":
            self.handler = handlers.Sr3RollHandler()
        else:
            return await ctx.send("That is an invalid mode")
        await ctx.send(f"Mode changed to {mode}")


def setup(bot):
    bot.add_cog(roller(bot))
