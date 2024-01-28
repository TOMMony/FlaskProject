import sqlite3

def display_stock():
    with sqlite3.connect("sqlite_db") as db:
        cursor = db.cursor()
        #sql = "SELECT points FROM user;"
        #sql = "SELECT name FROM sqlite_master WHERE type='table';"
        sql = "SELECT MAX(id) FROM schedule"
        cursor.execute(sql)
        course_name = "course"
        id = "user_id"

        print(cursor.fetchone()[0])

display_stock()


    