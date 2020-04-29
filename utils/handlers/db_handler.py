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

    def init_tables(self):
        """
        Initializes the tables used for the bot. These include
            commands: tracking how often commands are used in order to know
                      which commands would have the greatest impact if broken
                      or needing to be updated.
        """

        c = self.conn.cursor()
        c.execute('''CREATE TABLE if not exists commands (
                        id integer primary key autoincrement not null,
                        name varchar(30),
                        usage integer default 0,
                        unique(name)
                        )''')
        self.conn.commit()

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


class TagDB():
    """Handles connections to the database to store and get custom user tags"""

    def __init__(self, db="discord.db"):
        self.db = db
        self.conn = sqlite3.connect(self.db)

    def init_tables(self):
        """Initializes tables the bot will need.

            tags: Store of all user tags
        """

        c = self.conn.cursor()
        c.execute('''CREATE TABLE if not exists tags (
                        id integer primary key autoincrement not null,
                        user_id varchar(30),
                        tag varchar(100),
                        content varchar(2000),
                        unique(tag)
                        )''')
        self.conn.commit()

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
