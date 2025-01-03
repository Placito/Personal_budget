# import SQLlite
import sqlite3 as lite

# Creating connection
con = lite.connect('dados.db')

# Create tables
with con:
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE Category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)

with con:
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE Recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            added_in DATE,
            value DECIMAL
        )
    """)

with con:
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE Expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            removed_in DATE,
            value DECIMAL
        )
    """)
