import sqlite3

class Database:
    def __init__(self, db_name='fridge.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            expiration_date TEXT NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS dishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            eat_by_date TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def add_product(self, name, expiration_date):
        self.cursor.execute('INSERT INTO products (name, expiration_date) VALUES (?, ?)', (name, expiration_date))
        self.conn.commit()

    def add_dish(self, name, eat_by_date):
        self.cursor.execute('INSERT INTO dishes (name, eat_by_date) VALUES (?, ?)', (name, eat_by_date))
        self.conn.commit()

    def get_products(self):
        self.cursor.execute('SELECT name, expiration_date FROM products')
        return self.cursor.fetchall()

    def get_dishes(self):
        self.cursor.execute('SELECT name, eat_by_date FROM dishes')
        return self.cursor.fetchall()
