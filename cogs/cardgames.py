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


if __name__ == "__main__":
    # Do testing functions here
    # none are made yet....
    pass

else:
    def setup(bot):
        bot.add_cog(cardgames(bot))
