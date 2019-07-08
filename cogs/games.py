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

import random
from discord.ext import commands
import asyncio


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Rock Paper Scissors game")
    async def rps(self, ctx):
        """
        Simple rock paper scissors game.

        To start playing, type .rps

        Examples:
            Play Rock Paper Scissors:
            .rps
        """

        choices = ["rock", "scissors", "paper"]

        await ctx.send("Let's play rock papaer scissors. You have 3 choices\n"
                       "rock\npaper\nscissors\nReply with your choice.")

        choice = random.randint(0, 2)

        def pred(m):
            return (m.author == ctx.message.author and
                    m.channel == ctx.message.channel)

        msg = await self.bot.wait_for('message', check=pred, timeout=20)

        player_choice = msg.content

        try:
            winning = False
            player_choice = choices.index(player_choice)
            if player_choice == choice:
                winning = "tie"
            elif (player_choice + 1) % 3 == (choice):
                winning = True

            if winning == "tie":
                message = f"We tied. I chose {choices[choice]}"
            elif winning:
                message = f"I chose {choices[choice]}. You won! :smile:"
            else:
                message = f"I chose {choices[choice]}. You lost, try again!"
        except Exception as e:
            await ctx.send(f"Something went wrong.\nError:\n{e}")
        await ctx.send(message)

    @commands.command(description="Guess the number game")
    async def guess(self, ctx):
        """
        A simple game where the bot picks a number from 1 to 100 and you try
        guess it within 5 guesses.

        To begin, simply type .guess

        Examples:
            Start the game
            .guess

            Guess a number
            .guess 40
        """

        def check(m):
            return (m.author == ctx.message.author and
                    m.channel == ctx.message.channel and
                    m.content.startswith(".guess"))

        secret_num = random.randint(1, 101)
        tries = 5

        await ctx.send("I am thinking on a number from 1 to 100. Take a guess")

        while tries > 0:

            try:
                msg = await self.get_guess(ctx)

                command, guess = msg.content.split(" ")
                guess = int(guess)

                await ctx.send(msg.author)

                if guess == secret_num:
                    return await ctx.send("Congratulations! You guessed it.")

                elif guess > secret_num:
                    await ctx.send("That was too high. Please try again.")

                elif guess < secret_num:
                    await ctx.send("That was too low. Please try again.")

                tries -= 1

            except asyncio.TimeoutError:
                return await ctx.send("I'm sorry, you took too long to reply."
                                      "\nSimply run '.guess' to play again.")
            except ValueError:
                await ctx.send("I'm sorry, Something went wrong.\n"
                               "Please try again.")

            except IndexError:
                await ctx.send("Did you make a guess? I couldn't find the "
                               "number.")

        return await ctx.send("Better luck next time.")

    async def get_guess(self, ctx):
        def check(m):
            return (m.author == ctx.message.author and
                    m.channel == ctx.message.channel and
                    m.content.startswith(".guess"))

        return await self.bot.wait_for('message', check=check, timeout=60)


def setup(bot):
    bot.add_cog(Games(bot))
