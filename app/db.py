import sqlite3

DB_NAME = "Data/database.db"
DB = sqlite3.connect(DB_NAME)
DB_CURSOR = DB.cursor()

DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS Users(username TEXT PRIMARY KEY, password TEXT, country TEXT, currency TEXT);")

def add_user(username, password, country, currency):
    DB_NAME = "Data/database.db"
    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()
    DB_CURSOR.execute("SELECT COUNT(*) FROM Users WHERE username = (?)", (username,))
    cursorfetch = DB_CURSOR.fetchone()[0]
    if cursorfetch == 1:
        DB.commit()
        DB.close()
        return False
    DB_CURSOR.execute("INSERT INTO Users VALUES(?, ?, ?, ?)", (username, password, country, currency))
    DB.commit()
    DB.close()
    return True

def get_user(username):
    DB_NAME = "Data/database.db"
    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()
    DB_CURSOR.execute("SELECT * FROM Users WHERE username = ?", (username,))
    cursorfetch = DB_CURSOR.fetchone()
    return cursorfetch
