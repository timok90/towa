import sqlite3


class MySqliteDb(object):
    def __init__(self):
        self.test_var = 1
        self.connection = None

    def __del__(self):
        try:
            self.connection.close()
        except Exception as e:
            raise e

    def create_connection(self, db_file):
        """ Create a connection to the sqlite database"""

        connection = None

        try:
            connection = sqlite3.connect(db_file)
            print("Successfully connected to sqlite3")
        except sqlite3.Error as e:
            raise e
        finally:
            if connection:
                connection.close()


if __name__ == '__main__':
    db = MySqliteDb()
    db.create_connection(
        'C:\\Users\\timok\\Desktop\\TOWA\\Python\\sqlite\\pysqlite.db')
