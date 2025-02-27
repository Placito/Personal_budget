# This file contains the database connection class and methods for inserting, deleting, and fetching data.
# It provides an interface for interacting with the SQLite database used in the Personal Budget Management application.

import sqlite3 as lite
from PyQt5.QtWidgets import QMessageBox

# Database Connection Class
class Database:
    def __init__(self, db_name="dados.db"):
        """
        Initialize the database connection.
        """
        self.db_name = db_name
        self.con = lite.connect(self.db_name)
        self.con.row_factory = lite.Row  # To return data as dictionaries

    def execute_query(self, query, params=()):
        """
        Execute a query that modifies the database (e.g., INSERT, UPDATE, DELETE).
        """
        with self.con:
            cur = self.con.cursor()
            cur.execute(query, params)
            self.con.commit()
            return cur

    def fetchall_query(self, query, params=()):
        """
        Execute a query that retrieves data from the database (e.g., SELECT).
        """
        with self.con:
            cur = self.con.cursor()
            cur.execute(query, params)
            return cur.fetchall()

# Insert Methods
def insert_category(category_name):
    """
    Insert a new category into the Category table.
    """
    db = Database()
    query = "INSERT INTO Category (name) VALUES (?)"
    db.execute_query(query, (category_name,))

def insert_recipe(category, added_in, value):
    """
    Insert a new recipe into the Recipes table.
    """
    db = Database()
    query = "INSERT INTO Recipes (category, added_in, value) VALUES (?,?,?)"
    db.execute_query(query, (category, added_in, value))

def insert_expense(category, removed_in, value):
    """
    Insert a new expense into the Expenses table.
    """
    db = Database()
    query = "INSERT INTO Expenses (category, removed_in, value) VALUES (?,?,?)"
    db.execute_query(query, (category, removed_in, value))

# Delete Methods
def delete_recipe(recipe_id):
    """
    Delete a recipe from the Recipes table by its ID.
    """
    db = Database()
    query = "DELETE FROM Recipes WHERE id=?"
    db.execute_query(query, (recipe_id,))

def delete_expense(expense_id):
    """
    Delete an expense from the Expenses table by its ID.
    """
    db = Database()
    query = "DELETE FROM Expenses WHERE id=?"
    db.execute_query(query, (expense_id,))

# Fetching Data Methods
def see_category():
    """
    Fetch all categories from the Category table.
    """
    db = Database()
    return db.fetchall_query("SELECT * FROM Category")

def see_recipes():
    """
    Fetch all recipes from the Recipes table.
    """
    db = Database()
    return db.fetchall_query("SELECT * FROM Recipes")

def see_expenses():
    """
    Fetch all expenses from the Expenses table.
    """
    db = Database()
    return db.fetchall_query("SELECT * FROM Expenses")
