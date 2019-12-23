# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord.ext import commands


class cardgames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.interface = bot.cardgame_interface

    @commands.command(description="DnD bot roller")
    async def cardgame(self, ctx, game):
        """
        Starts a cardgame with the bot specified by game.

        Currently the only game allowed is blackjack. This is so I can at least
        get it up and running already. It also only allows playing against the
        dealer for now.
        """

        author = ctx.message.author

        if game.startswith("b"):
            sid = await self.interface.create_game(game, author)
            handler = self.interface.current_sessions[sid]
            await self.interface.start_game(sid)
            dealer_hand = handler.dealer.hand[0]
            player_hand = handler.players[1].hand
            await ctx.send("You may hit or stand.")
            await ctx.send(f"The dealer has a {dealer_hand}")
            await ctx.send(f"You have {[card.name for card in player_hand]}")

            await ctx.send("Would you like to split your hand? y/n")
            split = await self.get_response(ctx)
            split = split.content
            if " ".join(split).startswith("y"):
                await self.interface.pass_commands(author, "split")
                await ctx.send("You have split your hand into\n"
                               f"{handler.players[1].hand[0].value}\n"
                               f"{handler.players[1].split_hand[0].value}")
            else:
                await ctx.send("Your hand will not be split.")
        else:
            return await ctx.send("Only blackjack is curently available.")

        while await self.interface.is_playing(author):
            response = await self.get_response(ctx)
            response = response.content

            if response.startswith("h"):
                response = await self.interface.pass_commands(author, response)
                player_hand = handler.players[1].tally
                await ctx.send(f"Your hand is {player_hand}")
                if player_hand > 21:
                    return await ctx.send("Sorry, you bust! Better luck next "
                                          "time")

            elif response.startswith("st"):
                response = await self.interface.pass_commands(author, response)
                await ctx.send(response)
                # Player has chosen to stand
                if not handler.players[1].bust and (
                       handler.dealer.tally < handler.players[1].tally):
                    await handler.dealer_play()
                dealer_hand = handler.dealer.tally
                if not handler.dealer.bust and (
                       handler.dealer.tally > handler.players[1].tally):
                    return await ctx.send("Sorry, you lost. The dealer has "
                                          f"{dealer_hand} Best of luck next "
                                          "time.")
                else:
                    return await ctx.send("Congrats, you won!")

            if handler.players[1].split_hand and len(
                                handler.player[1].split_hand) < 2:
                await ctx.send("Would you like to switch to your other hand?")
                swap = await self.get_response(ctx)
                if "".join(swap).startswith("y"):
                    await self.interface.pass_commands(author, "swap")


    async def get_response(self, ctx):
        def check(m):
            return (m.author == ctx.message.author and
                    m.channel == ctx.message.channel)

        return await self.bot.wait_for('message', check=check, timeout=60)


if __name__ == "__main__":
    # Do testing functions here
    # none are made yet....
    pass

else:
    def setup(bot):
        bot.add_cog(cardgames(bot))
