import sqlite3
import logging

from datetime import datetime
from settings import DB_LOCATION, DEBUG


logger = logging.getLogger(__name__)


class Profile:
    """
    Creates a database connection and implements standard methods.
    """
    __DB_LOCATION = DB_LOCATION

    def __init__(self):
        try:
            self.connection = sqlite3.connect(Profile.__DB_LOCATION)
            self.cursor = self.connection.cursor()
            self.create_test_dataset()

        except sqlite3.Error:
            logger.critical(msg='sqlite3_Error', exc_info=DEBUG)
            raise sqlite3.Error

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()

        if isinstance(exc_value, Exception):
            self.connection.rollback()

        else:
            self.connection.commit()

        self.connection.close()

    def update_one_profile(self, new_data: tuple) -> None:
        """
        Update one line in the database.
        """
        self.create_table()
        self.cursor.execute(
            '''
            UPDATE Cookie SET cookie = ?, datetime_last_start = ?, number_starts = number_starts + 1 WHERE id = ?
            ''',
            new_data
        )

    def update_more_profiles(self, many_new_data: tuple[tuple]) -> None:
        """
        Update more lines in the database.
        """
        self.create_table()
        self.cursor.executemany(
            '''
            UPDATE Cookie SET cookie = ?, datetime_last_start = ?, number_starts = number_starts + 1 WHERE id = ?
            ''',
            many_new_data
        )

    def insert_one_profile(self, new_data: tuple) -> None:
        """
        Insert one line in the database.
        """
        self.create_table()
        self.cursor.execute(
            '''
            INSERT INTO Cookie (datetime_create) VALUES (?)
            ''',
            new_data
        )

    def insert_more_profiles(self, more_new_data: tuple[tuple]) -> None:
        """
        Insert more lines in the database.
        """
        self.create_table()
        self.cursor.executemany(
            '''
            INSERT INTO Cookie (datetime_create) VALUES (?)
            ''',
            more_new_data
        )

    def create_table(self) -> None:
        """
        Create a database table if it does not exist already.
        """
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS Cookie(
                id                  integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                datetime_create     text                              NOT NULL,
                cookie              text                                      ,
                datetime_last_start text                                      ,
                number_starts       integer             default       0
            )'''
        )

    def checking_data_availability(self) -> None | tuple:
        """
        Checks if there is data in the database.
        """
        return self.cursor.execute('SELECT * FROM Cookie').fetchone()

    def create_test_dataset(self) -> None:
        """
        Filling the database with test data.
        """
        self.create_table()

        if self.checking_data_availability() is None:
            for _ in range(15):
                self.cursor.execute(
                    '''INSERT INTO Cookie (datetime_create) VALUES (?)''',
                    (
                        datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                    )
                )

    def get_users_and_cookies(self) -> list | None:
        """
        Returns all available data in the database as `tuple(id, cookie)`.
        """
        if self.checking_data_availability() is not None:
            result = self.cursor.execute(
                '''SELECT id, cookie FROM Cookie'''
            )

            return result.fetchall()

    def commit(self):
        """
        Commit changes to database.
        """
        self.connection.commit()
