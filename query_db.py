# This script will allow you to see the contents of the database and add new values and run on the terminal python query_db.py
import sqlite3 as lite

def view_table_data(table_name):
    con = lite.connect("dados.db")
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
        for row in rows:
            print(row)

def add_category(category_name):
    con = lite.connect("dados.db")
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Category (name) VALUES (?)", (category_name,))
        con.commit()
        print(f"Category '{category_name}' added successfully.")

def add_recipe(category, added_in, value):
    con = lite.connect("dados.db")
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Recipes (category, added_in, value) VALUES (?,?,?)", (category, added_in, value))
        con.commit()
        print(f"Recipe added successfully: {category}, {added_in}, {value}")

def add_expense(category, removed_in, value):
    con = lite.connect("dados.db")
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Expenses (category, removed_in, value) VALUES (?,?,?)", (category, removed_in, value))
        con.commit()
        print(f"Expense added successfully: {category}, {removed_in}, {value}")

if __name__ == "__main__":
    # View data in tables
    print("Categories:")
    view_table_data("Category")
    print("\nRecipes:")
    view_table_data("Recipes")
    print("\nExpenses:")
    view_table_data("Expenses")

    # Add new categories
    categories = ["Travel", "Food", "Entertainment", "Rent", "Shopping", "Water", "Electricity", "Car", "Transportation, Salary"]
    for category in categories:
        add_category(category)
