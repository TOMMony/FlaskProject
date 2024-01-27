import sqlite3

def display_stock():
    with sqlite3.connect("sqlite_db") as db:
        cursor = db.cursor()
        sql = "SELECT name FROM sqlite_master WHERE type='table';"
        cursor.execute(sql)
        print(cursor.fetchall())

display_stock()


    