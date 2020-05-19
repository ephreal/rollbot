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
    """Creates the guild tag table"""
    def __init__(self, db="discord.db"):
        super().__init__(db)
        self.version = 2
        self.description = "creates the table guild_tags"""
        self.breaks = "gtag command will not function without this migration"

    def migrate(self):
        """Migrates the database to schema version 2. This means creating the
           guild_tags database"""

        if not self.requisites():
            raise ValueError

        guild_tags = """create table guild_tags (
                        id integer primary key autoincrement not null,
                        guild_id integer,
                        tag varchar(128),
                        content varchar(2000)
                        )"""

        cursor = self.connection.cursor()
        cursor.execute(guild_tags)
        self.upgrade_table_version("schema")
        self.upgrade_table_version('guild_tags')
        self.connection.commit()

    def revert(self):
        """Removes the guild_tags table and drops the schema level"""

        if not self.revert_requisites():
            raise ValueError

        sql = """drop table guild_tags"""
        cursor = self.connection.cursor()

        cursor.execute(sql)
        self.downgrade_table_version("schema")
        self.downgrade_table_version("guild_tags")
        self.connection.commit()

    def revert_requisites(self):
        """Verifies that the database is correctly formatted to revert."""
        version = self.get_schema_version()
        sql = """select * from guild_tags"""
        cursor = self.connection.cursor()

        try:
            cursor.execute(sql)
        except sqlite3.OperationalError:
            return False

        if version == 2:
            return True

        return False

    def requisites(self):
        """Verifies the database schema is equal to 1"""

        if self.get_schema_version() == 1:
            return True
