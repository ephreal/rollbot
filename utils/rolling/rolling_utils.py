# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


import random


async def check_roll_channel(ctx, bot):
    """
    ctx: discord.ext.commands.Context
    bot: discord.ext.command.Bot
        -> channel: discord.TextChannel
    """

    channel = ctx.channel

    if bot.restrict_rolling:
        channel = await get_roll_channel(ctx)

    return channel


async def get_roll_channel(ctx):
    """
    Gets the roll channel if rolling is restricted to rolling channels

    Checks to see if the context channel name is either 'rolling' or
    'bottesting'. This is to restrict rolling to just those channels.

    ctx: discord.ext.commands.Context
        -> channel: discord.TextChannel
    """

    allowed_channels = ["bottesting", "rolling"]
    roll_channel = ctx.channel
    name = ctx.channel.name

    # Check if this is a DM
    if not ctx.guild:
        return roll_channel

    # Otherwise check the rolling channel
    if name not in allowed_channels and "roll" not in name:
        for channel in ctx.guild.text_channels:
            if "roll" in channel.name.lower():
                roll_channel = channel
                break

    return roll_channel


async def roll(dice_pool=1, sides=6):
    # Weirdly, randrange seems to be way faster than randint
    return [random.randrange(sides) + 1 for _ in range(0, dice_pool)]


async def sr1_roll(dice_pool=1, sides=6):
    """Rolls dice according to sr1 rules"""
    rolls = [random.randrange(sides) + 1 for _ in range(0, dice_pool)]
    sixes = [x for x in rolls if x == 6]
    rolls = [x for x in rolls if x < 6]
    if sixes:
        sixes = [x+y for x, y in zip(sixes, await sr1_roll(len(sixes), 6))]
        rolls.extend(sixes)
    return rolls
