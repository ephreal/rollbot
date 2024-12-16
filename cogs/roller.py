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
import re


class Roller(commands.Cog):
    def __init__(self, bot):
        self.handlers = {
            "basic": handlers.BaseRollHandler(),
            "sr3": handlers.Sr3RollHandler(),
            "dnd": handlers.DndRollHandler(),
            "vm": handlers.VampireMasqueradeHandler(),
        }
        self.guild_handlers = {}  # In-memory storage for guild roll modes
        self.bot = bot

    def get_default_rollmode(self, ctx):
        """Get the default rollmode for the guild."""
        return self.guild_handlers.get(ctx.guild.id, 'sr3')

    def is_xdy_format(self, string):
        """Check if the string is in the 'XdY' format."""
        return bool(re.match(r'^\d+d\d+$', string))

    def determine_handler(self, roll_args, rollmode):
        """Determine the appropriate handler based on rollmode and input format."""
        if self.is_xdy_format(roll_args[0]) and rollmode not in ['basic', 'dnd']:
            return self.handlers['basic']
        
        return self.handlers.get(rollmode, self.handlers['sr3'])

    async def preprocess_roll_args(self, ctx, roll_args):
        """Preprocess the roll arguments and extract rollmode."""
        rollmode = self.get_default_rollmode(ctx)
        return roll_args, rollmode

    @commands.command(aliases=['r'])
    async def roll(self, ctx, *roll_args):
        """Rolls dice based on the specified game mode and arguments."""
        if not roll_args:
            return await ctx.send("Please provide a roll argument, e.g., `1d6`")

        roll_args, rollmode = await self.preprocess_roll_args(ctx, list(roll_args))

        # Check if we are in a roll channel
        channel = await rolling_utils.check_roll_channel(ctx, self.bot)

        if "-h" in roll_args:
            # Provide help if -h is used
            handler = self.handlers.get(rollmode, self.handlers['sr3'])
            message = handler.parser.format_help()
            return await ctx.send(f"```{message}```")

        # Determine the appropriate handler for the roll
        handler = self.determine_handler(roll_args, rollmode)

        try:
            roll = await handler.roll(roll_args)
            message = await roll.format()

            embed_color = Colour.red() if "CRITICAL" in message or "FAILURE" in message else Colour.green()
            message = await message_builder.embed_reply(ctx.author, message, embed_color)
            await channel.send(embed=message)
        except Exception as e:
            await ctx.send(f"An error occurred while rolling: {str(e)}")

    @commands.command(description="Sets current rolling mode")
    async def rollmode(self, ctx, mode):
        """Sets the current rolling mode.

        Valid options are "basic", "dnd", "sr3", and "vm"
        """
        modes = {
            "basic": "Basic rolling mode",
            "dnd": "Dungeons and Dragons",
            "sr3": "Shadowrun 3rd Edition",
            "vm": "Vampire the Masquerade Roller"
        }

        mode = mode.lower()

        if mode not in modes:
            return await ctx.send("That is an invalid mode")

        self.guild_handlers[ctx.guild.id] = mode
        await ctx.send(f"Mode changed to {modes[mode]}")


async def setup(bot):
    await bot.add_cog(Roller(bot))
