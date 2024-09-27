import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql
import psycopg2.errors


class DataBase:

    __slots__ = ("user_name", "password", "db_name", "host", "con", "cur")

    def __init__(self, user_name, password, db_name, host):
        self.user_name = user_name
        self.password = password
        self.db_name = db_name
        self.host = host

        self.con = psycopg2.connect(dbname='postgres',
                                    user=self.user_name,
                                    host=self.host,
                                    password=self.password)
        self.con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.con.cursor()


    def create_db(self) -> None:
        try:
            self.cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.db_name)))
            print(f"Database {self.db_name} has created successfully")
        except psycopg2.errors.DuplicateDatabase:
            print(f"Database {self.db_name} already exists. Nothing was changed.")

        self.con = psycopg2.connect(dbname=self.db_name,
                                    user=self.user_name,
                                    host=self.host,
                                    password=self.password)
        self.con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.con.cursor()


    def drop_db(self) -> None:
        self.con = psycopg2.connect(dbname='postgres',
                                    user=self.user_name,
                                    host=self.host,
                                    password=self.password)
        self.con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.con.cursor()
        try:
            self.cur.execute(sql.SQL("DROP DATABASE {} WITH (FORCE)").format(sql.Identifier(self.db_name)))
        except psycopg2.errors.InvalidCatalogName:
            print(f"Table {self.db_name} doesnt exists. Nothing was changed.")


    def create_table(self, table_name: str, columns: list) -> None:
        sql_prompt = (f"CREATE TABLE {table_name}\n"
                      f"(\n")
        for i in range(len(columns)-1):
            sql_prompt += columns[i][0] + ' ' + columns[i][1] + ",\n"
        sql_prompt += columns[-1][0] + ' ' + columns[-1][1] + "\n"
        sql_prompt += ");"
        try:
            self.cur.execute(sql.SQL(sql_prompt))
            print(f"Table {table_name} has created successfully")
        except psycopg2.errors.DuplicateTable:
            print(f"Table {table_name} already exists. Nothing was changed.")


    def drop_table(self, table_name: str) -> None:
        try:
            self.cur.execute(sql.SQL("DROP TABLE {}").format(sql.Identifier(table_name)))
            print(f"Table {table_name} has deleted successfully")
        except psycopg2.errors.UndefinedTable:
            print(f"Table {table_name} doesnt exists. Nothing was changed.")


    def add_columns(self, table_name: str, columns: list) -> None:
        for column in columns:
            try:
                self.cur.execute(sql.SQL(f"ALTER TABLE {table_name} ADD COLUMN {column[0]} {column[1]}"))
            except psycopg2.errors.DuplicateColumn:
                print(f"Column {column[0]} already exists. Nothing was changed.")
        print(f"Columns has added successfully")


# --------------------------------------------FAST-TESTS-------------------------------------------------

columns = [['a', 'int'], ['b', 'varchar(64)']]
new_columns = [['kaokoak', 'int']]

db = DataBase('postgres', '123', 'vk_data', '127.0.0.1')
db.drop_db()
db.create_db()
db.create_table('oudap', columns)
db.add_columns('oudap', new_columns)
db.drop_table('oudap')
db.drop_db()
db.drop_db()
