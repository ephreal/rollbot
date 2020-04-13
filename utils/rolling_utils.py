# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


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

    # Check if this is a DM
    if not ctx.guild:
        return roll_channel

    # Otherwise check the rolling channel
    if ctx.channel.name not in allowed_channels:
        for channel in ctx.guild.text_channels:
            if "roll" in channel.name.lower():
                roll_channel = channel
                break

    return roll_channel
