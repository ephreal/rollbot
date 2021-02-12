# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from sqlite3 import OperationalError
from utils.db.migrations.abc import abc_migration


class Migration(abc_migration.Migration):
    """Creates the shadowland tables and views"""
    def __init__(self, db="discord.db"):
        super().__init__(db)
        self.version = 3
        self.description = "Sets up the shadowland bbs table"""
        self.breaks = "All shadowland bbs functionality requires this."

    def migrate(self):
        """Migrates the database to schema version 3. This means creating the
           shadowland database"""

        if not self.requisites():
            raise ValueError

        # I'd like these to be specific to each discord guild. Hence the guild
        # id there. Note that each guild should only have one entry in the
        # shadowland table.
        # Organization is
        # shadowland_bbs: points to the correct threads for the bbs
        # shadowland_threads: Consists of posts in that thread
        # shadowland_posts: Author/text info of each post

        shadowland_bbs = """create table shadowland_bbs(
                         id integer primary key autoincrement not null,
                         guild int
                         )"""

        shadowland_thread = """create table shadowland_thread(
                            id integer primary key autoincrement not null,
                            name varchar(128) unique,
                            bbs int,
                            foreign key(bbs) references shadowland_bbs(id)
                            )"""
        shadowland_post = """
                          create table shadowland_post (
                          id integer primary key autoincrement not null,
                          user varchar(32),
                          content varchar(200),
                          thread int,
                          foreign key(thread) references shadowland_thread(id)
                          )
                           """
        shadowland_user = """create table shadowland_user(
                          id integer primary key autoincrement not null,
                          user int,
                          name varchar(64),
                          guild int
                          )
                          """

        cursor = self.connection.cursor()
        # I'm going to update the schema immediately so that I can revert any
        # changes later just in case this fails to apply completely.
        # In fact... I should add in a check_upgrade_status() method to the
        # abc and declare which tables should exist at each level.
        self.upgrade_table_version("schema")
        self.connection.commit()

        cursor.execute(shadowland_bbs)
        cursor.execute(shadowland_thread)
        cursor.execute(shadowland_post)
        cursor.execute(shadowland_user)

        self.upgrade_table_version("shadowland_bbs")
        self.upgrade_table_version("shadowland_thread")
        self.upgrade_table_version("shadowland_post")
        self.upgrade_table_version("shadowland_user")
        self.connection.commit()

        self.migrated = True

    def revert(self):
        """Removes all shadowland tables and drops the schema level"""

        if not self.revert_requisites():
            raise ValueError

        cursor = self.connection.cursor()

        # We gotta run this in reverse here... posts reference threads, etc.
        tables = ["shadowland_post", "shadowland_thread", "shadowland_bbs",
                  "shadowland_user"]
        for table in tables:
            try:
                cursor.execute(f"drop table {table}")
            except OperationalError:
                pass
            self.downgrade_table_version(table)
            self.connection.commit()

        self.downgrade_table_version("schema")

        self.migrated = False

    def revert_requisites(self):
        """Verifies that the database is correctly formatted to revert."""
        version = self.get_schema_version()

        if version == 3:
            return True

        return False

    def requisites(self):
        """Verifies the database schema is equal to 1"""

        tables = ["shadowland_bbs", "shadowland_thread", "shadowland_post",
                  "shadowland_user"]

        # Ensure that a migration did not fail midway.
        if self.failed_migration_pending(tables):
            self.revert()

        if self.get_schema_version() == 2:
            return True
