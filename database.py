import sqlite3


class MySqliteDb(object):
    def __init__(self):
        self.test_var = 1
        self.connection = None
        self.cursor = None
        self.logging_table = False

        self._create_connection()
        self._create_cursor()


    def __del__(self):
        try:
            self.connection.close()
        except Exception as e:
            raise e

    def _create_connection(self, db_file):
        """ Create a connection to the sqlite database"""

        # connection = None

        try:
            self.connection = sqlite3.connect(db_file)
            print("Successfully connected to sqlite3")
        except sqlite3.Error as e:
            raise e

        return self.connection

    def _create_cursor(self):
        """Creates Cursor object for sqlite db """
        try:

        except sqlite3.Error as e:
            raise e

    def create_logging_table(self, tablename):
        """Creates the table for logging the html accesses"""
        pass

        #TODO: improve the check if table already exists by e.g. db query

        if not self.logging_table:
            # create the table
            try:
                cursor = self.connection.cursor()

        else:
            msg = f"table {tablename} already exists"
            return msg


if __name__ == '__main__':
    db = MySqliteDb()
    db.create_connection(
        'C:\\Users\\timok\\Desktop\\TOWA\\Python\\sqlite\\pysqlite.db')
    db.create_logging_table("LoggingTable")
