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
                    "sr3": handlers.Sr3RollHandler(),
                    "dnd": handlers.DndRollHandler()
        }
        self.guild_handlers = {}
        self.db = bot.db_handler.guilds
        self.bot = bot

    @commands.command(aliases=['r'])
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

        roll_args, handler = await self.get_handler(ctx, list(roll_args))

        channel = await rolling_utils.check_roll_channel(ctx, self.bot)
        if "-h" in roll_args:
            message = handler.parser.format_help()
            message = f"```{message}```"
            return await ctx.send(message)

        roll = await handler.roll(roll_args)
        message = await roll.format()

        if "CRITICAL" in message or "FAILURE" in message:
            message = await message_builder.embed_reply(ctx.author, message,
                                                        Colour.red())
        else:
            message = await message_builder.embed_reply(ctx.author, message,
                                                        Colour.green())

        await channel.send(embed=message)

    @commands.command(description="Sets current rolling mode")
    async def game(self, ctx, mode):
        """Sets the current rolling mode.

        Valid options are "basic", "dnd", and "sr3"
        """

        modes = {
            "basic": "Basic rolling mode",
            "dnd": "Dungeons and Dragons",
            "sr3": "Shadowrun 3rd Edition",
        }

        mode = mode.lower()

        if mode == "basic":
            await self.db.set_roll_handler(ctx.guild.id, "basic")
            self.guild_handlers[ctx.guild.id] = "basic"

        elif mode == "dnd":
            await self.db.set_roll_handler(ctx.guild.id, "dnd")
            self.guild_handlers[ctx.guild.id] = "dnd"

        elif mode == "sr3":
            await self.db.set_roll_handler(ctx.guild.id, "sr3")
            self.guild_handlers[ctx.guild.id] = "sr3"
        else:
            return await ctx.send("That is an invalid mode")
        await ctx.send(f"Mode changed to {modes[mode]}")

    async def get_handler(self, ctx, roll_args):
        if "-g" in roll_args:
            index = roll_args.index("-g")
            roll_args.pop(index)
            handler = roll_args.pop(index)
        else:

            try:
                handler = self.guild_handlers[ctx.guild.id]
            except KeyError:
                handler = await self.db.get_roll_handler(ctx.guild.id)
                self.guild_handlers[ctx.guild.id] = handler

        handler = self.handlers[handler]
        return tuple(roll_args), handler


def setup(bot):
    bot.add_cog(roller(bot))
