import discord
from discord import client
from discord.utils import get


class utils():
    def __init__(self, bot):
        self.bot = bot
        self.rolls = {}

    async def check_channel(self, ctx, roll_channels):
        """
        Verifies that bot is allowed to send the output
        of roll commands to this channel.
        """

        author = ctx.message.author
        channel = ctx.message.channel.name
        server = ctx.message.server

        # Return the channel if pm
        if ctx.message.channel.is_private:
            return ctx.message.channel

        # Return the current channel if no rolling channels are defined
        if not roll_channels:
            return ctx.message.channel

        if channel not in roll_channels:
            # PM author if in wrong channel
            await self.bot.send_message(author,
                                        "Please limit shadowrun commands to"
                                        "the rolling or bottesting channels.\n"
                                        "The results of your command will be"
                                        "found in the rolling channel")

            await client.Client.delete_message(self.bot, ctx.message)

            # Return the rolling channel
            # channel = client.Client.get_channel(self.bot,id=roll_channels[0])
            channel = get(server.channels, name=roll_channels[0],
                          type=discord.ChannelType.text)

            command = ctx.message.content
            await self.bot.send_message(channel,
                                        f"Command was \"{command}\"")
            return channel

        else:
            return ctx.message.channel

    async def add_roll(self, author_id, roll):
        """
        Adds an author id/roll combination to self.rolls to allow rerolling of
        dice at a later time.
        """

        self.rolls[author_id] = roll

    async def last_roll(self, author_id):
        """
        Retrieves the last roll that was rolled by "author_id"
        """

        try:
            return self.rolls[author_id]
        except KeyError:
            return None
