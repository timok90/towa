import sqlite3


class MySqliteDb(object):
    def __init__(self):
        self.test_var = 1
        self.connection = None
        self.cursor = None
        self.logging_table = False
        self.tablename = None

        self._create_connection(
            "C:\\Users\\timok\\Desktop\\TOWA\\Python\\sqlite\\pysqlite.db")
        self._create_cursor()
        self.string_createLoggingTable = ""

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
            self.cursor = self.connection.cursor()

        except sqlite3.Error as e:
            raise e

    def create_logging_table(self, tablename):
        """Creates the table for logging the html accesses"""
        pass

        #TODO: improve the check if table already exists by e.g. db query

        if not self.logging_table:
            # create the table
            try:
                cursor = self.cursor
                self.string_createLoggingTable = self._sql_command_createLoggingTable(
                    tablename)
                cursor.execute(self.string_createLoggingTable)
                self.connection.commit()
                self.logging_table = True
                self.tablename = tablename

                msg = f"Table {tablename} was created"
                print(msg)
            except sqlite3.Error as e:
                raise e

        else:
            msg = f"table {tablename} already exists"
            print(msg)

    def _sql_command_createLoggingTable(self, tablename):
        sql_String = f"""CREATE TABLE IF NOT EXISTS {tablename} (
            remote_ip TEXT,
            timestamp INTEGER,
            protocol TEXT,
            host TEXT,
            path TEXT,
            query JSON
             );"""
        return sql_String

    def _insert_logging_data(self, tablename, logging_data: dict):
        columns = ",".join(logging_data.keys())
        quest_str = ["?" for x in range(len(logging_data))]
        valu_string = ",".join(quest_str)

        values = [logging_data[x] for x in logging_data.keys()]

        sql_string = f""" INSERT INTO {tablename} ({columns}) VALUES({valu_string}) """

        try:
            self.cursor.execute(sql_string, values)
            self.connection.commit()
        except sqlite3.Error as e:
            raise e

        return None


if __name__ == '__main__':
    db = MySqliteDb()
    db.create_logging_table("LoggingTable")

    testdata = {"remote_ip": "127.1", "host": 123}
    db._insert_logging_data("LoggingTable", logging_data=testdata)
