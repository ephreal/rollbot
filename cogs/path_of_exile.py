# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import random
from discord.ext import commands
from utils.rolling import rolling_utils


class poe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rolls = {}

    @commands.command(pass_context=True)
    async def lab(self, ctx, amt: int):
        """
        A specific rolling command to get amt amount of distinct numbers
        ranging from 1 to 10, inclusive. As you'd expect, the largest number
        allowed is 10.
        """

        # Channel checks. Rolling is restricted to a few channels
        # on my discord server.
        channel = await rolling_utils.get_roll_channel(ctx)

        try:

            amt = int(amt)

            if amt > 10 or amt < 1:
                return await ctx.send("I'm sorry, going larger than 10 or less"
                                      " than one makes no sense")
            else:
                sample = random.sample([x for x in range(1, 11)], amt)

            sample.sort()
            await channel.send(sample)

        except Exception as e:
            await channel.send("Incorrect input. Run .help lab if you need "
                               "help.")
            await channel.send(f"Error message: {e}")


def setup(bot):
    bot.add_cog(poe(bot))
