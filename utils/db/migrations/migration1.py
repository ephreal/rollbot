# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import sqlite3
from utils.db.migrations.abc import abc_migration


class Migration(abc_migration.Migration):
    """Creates a guild_config table, transfers all data in greetings to config,
       and then drops greetings."""
    def __init__(self, db="discord.db"):
        super().__init__(db)
        self.version = 1
        self.description = "creates guild_config and copies greetings to it."""
        self.breaks = "Breaks greetings until database is fully updated"

    def migrate(self):
        """
        Migrates the database
        """

        if not self.requisites():
            raise ValueError

        cursor = self.connection.cursor()
        config = """create table if not exists guild_config (
                        id integer primary key autoincrement not null,
                        guild_id integer,
                        message varchar(2000) default null,
                        active integer default 0,
                        roll_type varchar (10),
                        unique (guild_id)
                        )"""

        transfer = """insert into guild_config (guild_id, message, active)
                      select guild_id,message,active from greetings"""

        remove_old = """drop table greetings"""

        remove_version = """delete from db_versions where db='greetings'"""

        cursor.execute(config)
        self.connection.commit()
        cursor.execute(transfer)
        cursor.execute(remove_old)
        cursor.execute(remove_version)
        self.upgrade_table_version("guild_config")
        self.upgrade_table_version("schema")
        self.connection.commit()

    def revert(self):
        """
        reverts the database to the previous state.
        """

        if not self.revert_requisites():
            raise ValueError

        cursor = self.connection.cursor()
        greetings = '''CREATE TABLE if not exists greetings (
                        id integer primary key autoincrement not null,
                        guild_id integer,
                        message varchar(2000) default null,
                        active integer default 0,
                        unique (guild_id)
                        )'''

        transfer = """insert into greetings (guild_id, message, active)
                      select guild_id,message,active from guild_config"""

        remove = '''DROP TABLE guild_config'''

        cursor.execute(greetings)
        self.connection.commit()
        cursor.execute(transfer)
        cursor.execute(remove)
        self.downgrade_table_version("guild_config")
        self.downgrade_table_version("schema")
        self.upgrade_table_version("greetings")
        self.connection.commit()

    def revert_requisites(self):
        """
        Ensures the greetings table does not exist and that the databse schema
        is 1.
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute("select * from greetings")
            return False
        except sqlite3.OperationalError:
            pass

        cursor.execute("select version from db_versions where db='schema'")
        version = cursor.fetchall()[0][0]

        if version == self.version:
            return True
        return False

    def requisites(self):
        """
        Verifies that the greetings database is at version 0
        """
        cursor = self.connection.cursor()
        sql = """select version from db_versions where db='greetings'"""
        cursor.execute(sql)
        version = cursor.fetchall()[0][0]
        if version == 0:
            return True
        return False
