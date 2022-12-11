# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import random
from discord.ext import commands
import asyncio


class Games(commands.Cog):
    """
    .guess
    .rps
    """
    def __init__(self, bot):
        self.bot = bot

    async def get_guess(self, ctx):
        def check(m):
            return (m.author == ctx.message.author and
                    m.channel == ctx.message.channel)

        return await self.bot.wait_for('message', check=check, timeout=60)

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
            40
        """

        secret_num = random.randint(1, 101)
        tries = 5

        await ctx.send("I am thinking on a number from 1 to 100. Take a guess")

        while tries > 0:

            try:
                msg = await self.get_guess(ctx)

                guess = msg.content
                if guess == "quit":
                    return ctx.send("```Try playing again sometime!```")

                guess = int(guess)

                message = f'```\nRan by: {msg.author.name}\n'

                if guess == secret_num:
                    message += "Congratulations! You guessed it.\n```"
                    return await ctx.send(message)

                elif guess > secret_num and tries > 1:
                    message += "That was too high. Please try again.\n"

                elif guess < secret_num and tries > 1:
                    message += "That was too low. Please try again.\n"

                message += "```"

                await ctx.send(message)
                tries -= 1

            except asyncio.TimeoutError:
                return await ctx.send("``\n"
                                      "I'm sorry, you took too long to reply."
                                      "\nSimply run '.guess' to play again."
                                      "\n```")
            except ValueError:
                await ctx.send("```\nI'm sorry, Something went wrong.\n"
                               "Please try again.\n```")

            except IndexError:
                await ctx.send("```\nDid you make a guess? I couldn't find "
                               "the number.\n```")

        return await ctx.send("```\nBetter luck next time.\n```")

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

        await ctx.send("```css\n"
                       "Let's play rock paper scissors. You have 3 choices\n"
                       "rock\npaper\nscissors\nReply with your choice.```")

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
                message = f"```css\nWe tied. I chose {choices[choice]}```"
            elif winning:
                message = f"```css\nI chose {choices[choice]}. You won! " \
                          "```\n:smile:"
            else:
                message = f"```css\nI chose {choices[choice]}. You lost, " \
                          "try again!```"
        except Exception as e:
            await ctx.send(f"```css Something went wrong.\nError:\n{e}```")
        await ctx.send(message)


async def setup(bot):
    await bot.add_cog(Games(bot))
