import sqlite3 as lite

class Database:
    def __init__(self, db_name="dados.db"):
        self.db_name = db_name
        self.con = lite.connect(self.db_name)
        self.con.row_factory = lite.Row  # To return data as dictionaries

    def execute_query(self, query, params=()):
        with self.con:
            cur = self.con.cursor()
            cur.execute(query, params)
            self.con.commit()
            return cur

    def fetchall_query(self, query, params=()):
        with self.con:
            cur = self.con.cursor()
            cur.execute(query, params)
            return cur.fetchall()

class CategoryModel(Database):
    def insert_category(self, category_name):
        query = "INSERT INTO Category (name) VALUES (?)"
        self.execute_query(query, (category_name,))

    def get_categories(self):
        return self.fetchall_query("SELECT * FROM Category")

class RecipesModel(Database):
    def insert_recipe(self, category, added_in, value):
        query = "INSERT INTO Recipes (category, added_in, value) VALUES (?,?,?)"
        self.execute_query(query, (category, added_in, value))

    def get_recipes(self):
        return self.fetchall_query("SELECT * FROM Recipes")

class ExpensesModel(Database):
    def insert_expense(self, category, removed_in, value):
        query = "INSERT INTO Expenses (category, removed_in, value) VALUES (?,?,?)"
        self.execute_query(query, (category, removed_in, value))

    def get_expenses(self):
        return self.fetchall_query("SELECT * FROM Expenses")
