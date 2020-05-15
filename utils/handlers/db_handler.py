# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import sqlite3


class MetricsDB():
    def __init__(self, db="discord.db"):
        self.db = db
        self.conn = sqlite3.connect(self.db)

    async def update_commands(self, name, value):
        """
        Insert values into the commands tale.

        values: dict
        """

        c = self.conn.cursor()
        # Ensure the row exists in the table.
        # Note to self: That comma in the binding after name is VERY important
        c.execute('''INSERT or ignore into commands (name) values (?)''',
                  (name, ))

        # Then update the usage
        c.execute('''update commands set usage = usage + ? where name = ?''',
                  (value, name,))

        self.conn.commit()

    async def get_all_usage(self):
        """
        Returns how often all commands in the database have been used.
        """

        c = self.conn.cursor()
        c.execute("select name, usage from commands order by usage desc")
        usage = c.fetchall()
        return usage

    async def get_usage(self, name):
        """
        Returns how often a command has been used
        """

        try:
            c = self.conn.cursor()

            c.execute('''select usage from commands where name = ?''', (name,))
            usage = c.fetchall()[0][0]
            return usage
        except IndexError:
            # The command must not exist
            return 0

    async def clear_usage(self, uses=1):
        """
        Clears out anything that has equal or fewer uses than uses. Default
        uses is 1.
        """
        c = self.conn.cursor()
        c.execute('''delete from commands where usage <= ?''', (uses, ))

    async def get_greeting_status(self, guild_id):
        """
        Gets the greeting status for the guild_id passed in

        Parameters
        ----------

        guild_id: :class:`int`
            An int representing a discord guild id
        """

        c = self.conn.cursor()
        # Ensure the row exists in the table.
        # Note to self: That comma in the binding after name is VERY important
        c.execute('''INSERT or ignore into guild_config (guild_id)
                     values (?)''', (guild_id, ))

        # Then update the usage
        c.execute('''select active from guild_config where guild_id = ?''',
                  (guild_id, ))
        self.conn.commit()

        c = c.fetchall()
        return c[0][0]

    async def get_greeting(self, guild_id):
        """
        Gets the greeting status for the guild_id passed in

        Parameters
        ----------

        guild_id: :class:`int`
            An int representing a discord guild id
        """

        c = self.conn.cursor()
        # Ensure the row exists in the table.
        # Note to self: That comma in the binding after name is VERY important
        c.execute('''INSERT or ignore into guild_config (guild_id)
                     values (?)''', (guild_id, ))

        # Then update the usage
        c.execute('''select message from guild_config where guild_id = ?''',
                  (guild_id, ))
        self.conn.commit()

        c = c.fetchall()
        return c[0][0]

    async def set_greeting_status(self, guild_id, status=0):
        """
        Enables or disables the greeting for that guild.

        Parameters
        ----------

        guild_id: :class:`int`
            An int representing a discord guild id

        status: :class:`int`
            May be a 0 (disabled) or a 1 (enabled)
        """

        c = self.conn.cursor()
        # Ensure the row exists in the table.
        # Note to self: That comma in the binding after name is VERY important
        c.execute('''INSERT or ignore into guild_config (guild_id)
                     values (?)''', (guild_id, ))

        # Then update the usage
        c.execute('''update guild_config set active = ? where guild_id = ?''',
                  (status, guild_id, ))

        self.conn.commit()

    async def clear_greeting(self, guild_id):
        """
        Clears the greeting for that guild.

        Parameters
        ----------

        guild_id: :class:`int`
            An int representing a discord guild id
        """

        c = self.conn.cursor()
        c.execute('''update guild_config set message = null where
                     guild_id = ?''', (guild_id, ))

        self.conn.commit()

    async def set_greeting(self, guild_id, greeting):
        """
        Sets the greeting for the guild.

        Parameters
        ----------

        guild_id: :class:`int`
            An int representing a discord guidl id

        greeting: :class:`string`
            A string containing the greeting for the guild. Max length: 2000
        """

        c = self.conn.cursor()
        # Ensure the row exists in the table.
        # Note to self: That comma in the binding after name is VERY important
        c.execute('''INSERT or ignore into guild_config (guild_id)
                     values (?)''', (guild_id, ))

        # Then update the usage
        c.execute('''update guild_config set message = ? where guild_id = ?''',
                  (greeting, guild_id, ))

        self.conn.commit()


class TagDB():
    """Handles connections to the database to store and get custom user tags"""

    def __init__(self, db="discord.db"):
        self.db = db
        self.conn = sqlite3.connect(self.db)

    async def create_tag(self, user_id, tag, content):
        """Adds a tag to the database"""

        c = self.conn.cursor()
        c.execute('''INSERT or replace into tags (user_id, tag, content)
                     values (?,?,?)''', (user_id, tag, content))
        self.conn.commit()

    async def delete_tag(self, user_id, tag):
        """Deletes a tag from the database"""

        c = self.conn.cursor()
        c.execute('''delete from tags where user_id=? and tag=?''',
                  (user_id, tag, ))
        self.conn.commit()

    async def fetch_tag(self, user_id, tag):
        """Fetches a tag from the database"""

        c = self.conn.cursor()
        c.execute('''select content from tags where user_id=? and tag=?''',
                  (user_id, tag, ))

        content = c.fetchall()
        if not content:
            return None

        return content[0][0]

    async def fetch_all_tags(self, user_id):
        """Returns all tags a user_id has"""
        c = self.conn.cursor()
        c.execute('''select tag from tags where user_id=?''', (user_id, ))
        tags = c.fetchall()

        if tags:
            return [tag[0] for tag in tags]
        else:
            return None
