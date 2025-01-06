import sqlite3 as lite

# Creating connection
con = lite.connect('dados.db')

# insert operation
def insert_category(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Category (name) VALUES (?)"
        cur.execute(query, i)

def insert_recipes(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Recipes (category, added_in, value) VALUES (?,?,?)"
        cur.execute(query, i)

def insert_Expenses(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Expenses (category, removed_in, value) VALUES (?,?,?)"
        cur.execute(query, i)

# delete operations
def delete_recipes(i):
    with con:
        cur = con.cursor()
        query = query = "DELETE FROM Recipres WHERE id=?"
        cur.execute(query, i)

def delete_Expenses(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Expenses WHERE id=?"
        cur.execute(query, i)

# functions so we can see what we have inside the table

def see_category():
    list_items = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Category")
        rown = cur.fetchall()
        for l in rown:
            list_items.append(l)
    return list_items


print(see_category())
    
def see_recipes(i):
    list_items = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Recipes")
        rown = cur.fetchall()
        for l in rown:
            list_items.append(l)
    return list_items

def see_Expenses(i):
    list_items = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Expenses")
        rown = cur.fetchall()
        for l in rown:
            list_items.append(l)
    return list_items