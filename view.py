import sqlite3 as lite
from PyQt5.QtWidgets import QMessageBox

# Database Connection Class
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

# Insert Methods
def insert_category(category_name):
    db = Database()
    query = "INSERT INTO Category (name) VALUES (?)"
    db.execute_query(query, (category_name,))

def insert_recipe(category, added_in, value):
    db = Database()
    query = "INSERT INTO Recipes (category, added_in, value) VALUES (?,?,?)"
    db.execute_query(query, (category, added_in, value))

def insert_expense(category, removed_in, value):
    db = Database()
    query = "INSERT INTO Expenses (category, removed_in, value) VALUES (?,?,?)"
    db.execute_query(query, (category, removed_in, value))

# Delete Methods
def delete_recipe(recipe_id):
    db = Database()
    query = "DELETE FROM Recipes WHERE id=?"
    db.execute_query(query, (recipe_id,))

def delete_expense(expense_id):
    db = Database()
    query = "DELETE FROM Expenses WHERE id=?"
    db.execute_query(query, (expense_id,))

# Fetching Data Methods
def see_category():
    db = Database()
    return db.fetchall_query("SELECT * FROM Category")

def see_recipes():
    db = Database()
    return db.fetchall_query("SELECT * FROM Recipes")

def see_expenses():
    db = Database()
    return db.fetchall_query("SELECT * FROM Expenses")
