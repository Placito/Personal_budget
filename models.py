import sqlite3 as lite
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class for declarative models
Base = declarative_base()

# Category Model
class Category(Base):
    __tablename__ = 'Category'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Recipes Model
class Recipes(Base):
    __tablename__ = 'Recipes'
    
    id = Column(Integer, primary_key=True)
    category = Column(String)
    added_in = Column(String)
    value = Column(Float)

# Expenses Model
class Expenses(Base):
    __tablename__ = 'Expenses'
    
    id = Column(Integer, primary_key=True)
    category = Column(String)
    removed_in = Column(String)
    value = Column(Float)

# Database class for interacting with the SQLite database
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

    def get_total_income(self):
        query = "SELECT SUM(value) as total_income FROM Recipes"
        result = self.fetchall_query(query)
        return result[0]['total_income'] if result[0]['total_income'] else 0

    def get_total_expenses(self):
        query = "SELECT SUM(value) as total_expenses FROM Expenses"
        result = self.fetchall_query(query)
        return result[0]['total_expenses'] if result[0]['total_expenses'] else 0

# Category Model for interacting with the database
class CategoryModel(Database):
    def insert_category(self, category_name):
        query = "INSERT INTO Category (name) VALUES (?)"
        self.execute_query(query, (category_name,))

    def get_categories(self):
        return self.fetchall_query("SELECT * FROM Category")

# Recipes Model for interacting with the database
class RecipesModel(Database):
    def insert_recipe(self, category, added_in, value):
        query = "INSERT INTO Recipes (category, added_in, value) VALUES (?,?,?)"
        self.execute_query(query, (category, added_in, value))

    def get_recipes(self):
        return self.fetchall_query("SELECT * FROM Recipes")

# Expenses Model for interacting with the database
class ExpensesModel(Database):
    def insert_expense(self, category, removed_in, value):
        query = "INSERT INTO Expenses (category, removed_in, value) VALUES (?,?,?)"
        self.execute_query(query, (category, removed_in, value))

    def get_expenses(self):
        return self.fetchall_query("SELECT * FROM Expenses")
