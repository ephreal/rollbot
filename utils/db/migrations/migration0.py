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
    def __init__(self, db="discord.db"):
        super().__init__(db)
        self.version = 0
        self.description = "Initial configuration of the database"

    def migrate(self):
        """
        Creates 3 tables: commands, greeting, and tags
        """

        cursor = self.connection.cursor()

        commands = '''CREATE TABLE if not exists commands (
                        id integer primary key autoincrement not null,
                        name varchar(30),
                        usage integer default 0,
                        unique(name)
                        )'''

        greetings = '''CREATE TABLE if not exists greetings (
                        id integer primary key autoincrement not null,
                        guild_id integer,
                        message varchar(2000) default null,
                        active integer default 0,
                        unique (guild_id)
                        )'''

        tags = '''CREATE TABLE if not exists tags (
                        id integer primary key autoincrement not null,
                        user_id varchar(30),
                        tag varchar(100),
                        content varchar(2000),
                        unique(tag)
                        )'''

        version = '''create table if not exists db_versions (
                    db varchar (64),
                    version integer,
                    unique(db)
        )'''

        command_version = """insert or ignore into db_versions(db,version)
                                values ('commands', 0)
                            """

        greeting_version = """insert or ignore into db_versions(db,version)
                                values ('greetings', 0)"""

        tag_version = """insert or ignore into db_versions(db,version) values
                            ('tags', 0)
                         """

        db_version = """insert or ignore into db_versions(db,version) values
                            ('version', 0)"""

        schema_version = """insert or ignore into db_versions(db,version)
                            values ('schema', 0)"""

        cursor.execute(commands)
        cursor.execute(greetings)
        cursor.execute(tags)
        cursor.execute(version)
        cursor.execute(command_version)
        cursor.execute(greeting_version)
        cursor.execute(tag_version)
        cursor.execute(db_version)
        cursor.execute(schema_version)
        self.connection.commit()

    def revert(self):
        """
        Removes the tables
        """

        if not self.revert_requisites():
            raise ValueError

        commands = "drop table commands"
        greetings = "drop table greetings"
        tags = "drop table tags"
        db = "drop table db_versions"
        cursor = self.connection.cursor()

        cursor.execute(commands)
        cursor.execute(greetings)
        cursor.execute(tags)
        cursor.execute(db)

        self.connection.commit()

    def revert_requisites(self):
        """
        Returns True if the database version for all tables == 0
        """

        cursor = self.connection.cursor()

        versions = []

        commands_version = """select version from db_versions where
                                db='commands'"""
        greetings_version = """select version from db_versions where
                                db='greetings'"""
        tags_version = """select version from db_versions where
                                db='tags'"""
        db_version = """select version from db_versions where
                                db='version'"""
        try:
            cursor.execute(commands_version)
            versions.append(cursor.fetchall()[0][0])

            cursor.execute(greetings_version)
            versions.append(cursor.fetchall()[0][0])

            cursor.execute(tags_version)
            versions.append(cursor.fetchall()[0][0])

            cursor.execute(db_version)
            versions.append(cursor.fetchall()[0][0])

        except sqlite3.OperationalError:
            return False

        return sum(versions) == 0

    def requisites(self):
        """
        Always returns True. This migration is always safe to apply.
        """
        return True
