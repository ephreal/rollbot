# -*- coding: utf-8 -*-

"""
Copyright 2018 Ephreal

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

import aiohttp

from asyncio import sleep
from discord.ext import commands


class utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timers = []

    @commands.command(description="Timer/Reminder")
    async def timer(self, ctx):
        """
        Sets a timer

        timer sets a timer for X minutes/seconds/hours that messages you
        when time is up. This assumes seconds if you do not pass in a
        length value. The maximum available time you may set a timer for is
        3 hours.

        usage:
            30 second timer: .timer 30 s
                             .timer 30
            10 minute timer: .timer 10 m
            1 hour timer:    .timer 1 h
        """

        author = ctx.message.author
        command = ctx.message.content.lower().split()
        command = command[1:]

        valid_intervals = {
                            "s": 1,
                            "m": 60,
                            "h": 3600
                          }

        try:
            if len(command) == 0:
                return await ctx.send("How long do you want a timer set for?\n"
                                      "See '.help timer' for more info.")

            elif len(command) == 1:
                await ctx.send(f"Assuming {command[0]} seconds.")
                command.append("s")

            if command[1] not in list(valid_intervals.keys()):
                await ctx.send(f"Unknown length {command[1]}\n"
                               "assuming seconds...")
                await ctx.send(f"{command}")
                command[1] = 's'

            timer = int(command[0])
            interval = command[1]

            timer *= valid_intervals[interval]

            if timer > (3600 * 3):
                return await ctx.send("Max time allowed is 3 hours.")

            await ctx.send(f"Timer set for {command[0]} {command[1]}")

            await sleep(timer)

            await author.send("Timer is up!")

        except Exception as e:
            await ctx.send("Invalid input received.")
            await ctx.send(f"Error follows:\n{e}")

    @commands.command(description="gets a random 'inspirational' quote")
    async def quote(self, ctx, amount=1):
        """
        Gets a random quote created by inspirobot.me

        It's also possible to get multiple quotes.

        Note: I am not responsible for anything the
        inspirobot creates and sends to you. If you
        are easily offended, this may not be for
        you.

        usage:
            .quote

            Get 5 quotes
            .quote 5
        """

        url = "https://inspirobot.me/api?generate=true"

        if amount:

            try:
                amount = int(amount)

                if amount == 0:
                    amount = 1

                elif amount > 20:
                    amount = 20

                for i in range(0, amount):
                    quote = await self.get_quote(url)
                    await ctx.send(f"{i+1}\n{quote}")
                    if i == amount-1:
                        break
                    await sleep(7)

                # Let the caller know that quote grabbing
                # is complete when there are multiple quotes
                if amount > 1:
                    await ctx.send("Quote grabbing complete.")

            except Exception as e:
                await ctx.send(f"I'm sorry, an error occured.\n{e}\n"
                               "Here is a single quote")
                quote = self.get_qoute(url)
                await ctx.send(quote)
        else:
            quote = self.get_quote(url)
            await ctx.send(quote)

    async def get_quote(self, url):
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, url)
            return html

    async def fetch(self, session, url):
        async with session.get(url) as html:
            return await html.text()


def setup(bot):
    bot.add_cog(utils(bot))
