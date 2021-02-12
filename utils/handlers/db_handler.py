# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import sqlite3


class DBHandler():
    def __init__(self, db="discord.db"):
        self.db = db
        self.connection = sqlite3.connect(self.db)
        self.metrics = MetricsDB(self.connection)
        self.tags = TagDB(self.connection)
        self.guilds = GuildConfigDB(self.connection)
        self.shadowland = ShadowlandDB(self.connection)


class GuildConfigDB():
    def __init__(self, connection=None):
        self.conn = connection

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

    async def set_roll_handler(self, guild_id, roll_handler):
        """
        Sets the default roll handler for the discord guild.
        """

        cursor = self.conn.cursor()
        # Ensure the guild_id is in guild_config
        sql = """insert or ignore into guild_config (guild_id) values (?)"""
        cursor.execute(sql, (guild_id, ))
        self.conn.commit()

        sql = """update guild_config set roll_type=? where guild_id=?"""
        cursor.execute(sql, (roll_handler, guild_id, ))
        self.conn.commit()

    async def get_roll_handler(self, guild_id):
        """
        Returns the roll_type stored in guild_config. If there is None, basic
        is inserted and then returned.
        """

        cursor = self.conn.cursor()
        sql = "select roll_type from guild_config where guild_id=?"

        try:
            cursor.execute(sql, (guild_id, ))
            roll_type = cursor.fetchall()[0][0]
            if roll_type is None:
                await self.set_roll_handler(guild_id, "basic")
                roll_type = "basic"

        except IndexError:
            await self.set_roll_handler(guild_id, "basic")
            roll_type = "basic"

        return roll_type


class MetricsDB():
    def __init__(self, connection=None):
        if connection is None:
            return
        self.conn = connection

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
        amt = await self.get_usage(name)

        if amt <= 0:
            c.execute("delete from commands where name=?", (name, ))
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


class TagDB():
    """Handles connections to the database to store and get custom user tags"""

    def __init__(self, connection=None):
        self.conn = connection

    async def create_tag(self, user_id, tag, content):
        """Adds a tag to the database"""

        c = self.conn.cursor()
        c.execute('''INSERT or replace into tags (user_id, tag, content)
                     values (?,?,?)''', (user_id, tag, content))
        self.conn.commit()

    async def create_guild_tag(self, guild_id, tag, content):
        """Inserts a tag to the guild_tags table"""

        c = self.conn.cursor()
        c.execute('''INSERT or replace into guild_tags (guild_id, tag, content)
                     values (?,?,?)''', (guild_id, tag, content))
        self.conn.commit()

    async def delete_tag(self, user_id, tag):
        """Deletes a tag from the database"""

        c = self.conn.cursor()
        c.execute('''delete from tags where user_id=? and tag=?''',
                  (user_id, tag, ))
        self.conn.commit()

    async def delete_guild_tag(self, guild_id, tag):
        """Deletes a tag from the guild_tag table"""

        c = self.conn.cursor()
        c.execute('''delete from guild_tags where guild_id=? and tag=?''',
                  (guild_id, tag, ))
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

    async def fetch_guild_tag(self, guild_tag, tag):
        """Fetches a tag from the guild_tag table"""

        c = self.conn.cursor()
        c.execute('''select content from guild_tags where guild_id=? and
                     tag=?''', (guild_tag, tag, ))

        content = c.fetchall()
        if not content:
            return None

        return content[0][0]

    async def fetch_all_tags(self, user_id, offset=0):
        """Returns 50 tags a user_id has"""
        c = self.conn.cursor()
        sql = '''select tag from tags where user_id=?
                  order by tag
                  limit 25
                  offset ?'''
        c.execute(sql, (user_id, offset * 25))
        tags = c.fetchall()

        if tags:
            return [tag[0] for tag in tags]
        else:
            return None

    async def fetch_all_guild_tags(self, guild_id, offset=0):
        """Returns all tags a guild has"""
        c = self.conn.cursor()
        sql = '''select tag from guild_tags where guild_id=?
                 order by tag
                 limit 25
                 offset ?'''
        c.execute(sql, (guild_id, offset * 25))
        tags = c.fetchall()

        if tags:
            return [tag[0] for tag in tags]
        else:
            return None


class ShadowlandDB():
    def __init__(self, connection=None):
        self.conn = connection

    async def add_guild(self, guild_id):
        c = self.conn.cursor()
        sql = "insert into shadowland_bbs (guild) values (?)"
        c.execute(sql, (guild_id, ))
        self.conn.commit()

    async def add_user(self, guild_id, user_id, name):
        c = self.conn.cursor()
        sql = """insert into shadowland_user (user, guild, name)
                 values (?, ?, ?)"""
        c.execute(sql, (user_id, guild_id, name))
        self.conn.commit()

    async def check_guild(self, guild_id):
        c = self.conn.cursor()
        sql = "select guild from shadowland_bbs where guild = ?"
        c.execute(sql, (guild_id, ))

        data = c.fetchall()
        if not data:
            await self.add_guild(guild_id)

    async def get_bbs_username(self, guild_id, user_id):
        c = self.conn.cursor()
        sql = "select name from shadowland_user where guild=? and user=?"
        c.execute(sql, (guild_id, user_id))
        return c.fetchall()

    async def get_guild_bbs(self, guild_id):
        c = self.conn.cursor()
        sql = "select id from shadowland_bbs where guild=?"
        c.execute(sql, (guild_id, ))
        return c.fetchall()[0][0]

    async def create_thread(self, guild_id, name):
        await self.check_guild(guild_id)
        bbs_id = await self.get_guild_bbs(guild_id)
        c = self.conn.cursor()
        sql = """insert into shadowland_thread (name, bbs) values (?, ?)"""
        c.execute(sql, (name, bbs_id))
        self.conn.commit()
        return name

    async def get_threads(self, guild_id, page=0):
        await self.check_guild(guild_id)
        bbs_id = await self.get_guild_bbs(guild_id)
        c = self.conn.cursor()
        sql = """select name from shadowland_thread where bbs=?"""
        c.execute(sql, (bbs_id, ))
        return c.fetchall()

    async def create_post(self, thread_id, user, content):
        c = self.conn.cursor()
        sql = """insert into shadowland_post (thread, user, content)
                 values (?, ?, ?)"""
        c.execute(sql, (thread_id, user, content))
        self.conn.commit()

    async def get_thread_by_name(self, guild_id, name):
        bbs_id = await self.get_guild_bbs(guild_id)
        c = self.conn.cursor()
        sql = """select id from shadowland_thread where bbs = ? and name = ?"""
        c.execute(sql, (bbs_id, name))
        return c.fetchall()[0][0]
