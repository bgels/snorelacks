import sqlite3
import os
from datetime import datetime
import json

DB_NAME = "Data/database.db"
try:
    os.mkdir("Data/")
except:
    pass
DB = sqlite3.connect(DB_NAME)
DB_CURSOR = DB.cursor()
DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS Users(username TEXT PRIMARY KEY, password TEXT, country TEXT, currency TEXT);")
DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS Countries(country_name TEXT PRIMARY KEY, wiki_data TEXT, country_data TEXT, timestamp TEXT);")
DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS Favorites(username TEXT, country_name TEXT);")

def fav_country(country_name, username):
    DB_NAME = "Data/database.db"
    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()
    DB_CURSOR.execute("SELECT COUNT(*) FROM Favorites WHERE country_name = (?) AND username = (?)", (country_name, username))
    cursorfetch = DB_CURSOR.fetchone()[0]
    if cursorfetch == 1:
        DB.commit()
        DB.close()
        return False
    DB_CURSOR.execute("INSERT INTO Favorites VALUES(?, ?, ?)", (username, country_name))
    DB.commit()
    DB.close()
    return False

def get_favorites(username):
    DB_NAME = "Data/database.db"
    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()
    DB_CURSOR.execute("SELECT * FROM Favorites WHERE username = ?", (username,))
    cursorfetch = DB_CURSOR.fetchall()
    return cursorfetch

def unfav_country(country_name, username):
    DB_NAME = "Data/database.db"
    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()
    DB_CURSOR.execute("SELECT COUNT(*) FROM Favorites WHERE country_name = (?) AND username = (?)", (country_name, username))
    cursorfetch = DB_CURSOR.fetchone()[0]
    if cursorfetch != 1:
        DB.commit()
        DB.close()
        return False
    DB_CURSOR.execute("DELETE FROM Favorites where country_name = ? AND username = (?)", (country_name, username))
    DB.commit()
    DB.close()
    return True

def add_country(country_name, wiki_data, country_data):
    DB_NAME = "Data/database.db"
    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()
    DB_CURSOR.execute("SELECT COUNT(*) FROM Countries WHERE country_name = (?)", (country_name,))
    cursorfetch = DB_CURSOR.fetchone()[0]
    if cursorfetch == 1:
        DB.commit()
        DB.close()
        return False
    DB_CURSOR.execute("INSERT INTO Countries VALUES(?, ?, ?, ?)", (country_name, json.dumps(wiki_data), json.dumps(country_data), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    DB.commit()
    DB.close()
    return True

def get_country(country_name):
    DB_NAME = "Data/database.db"
    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()
    DB_CURSOR.execute("SELECT * FROM Countries WHERE country_name = ?", (country_name,))
    cursorfetch = DB_CURSOR.fetchone()
    return cursorfetch

def update_country(country_name, wiki_data, country_data):
    DB_NAME = "Data/database.db"
    DB = sqlite3.connect(DB_NAME)
    DB_CURSOR = DB.cursor()
    DB_CURSOR.execute("SELECT COUNT(*) FROM Countries WHERE country_name = (?)", (country_name,))
    cursorfetch = DB_CURSOR.fetchone()[0]
    if cursorfetch != 1:
        DB.commit()
        DB.close()
        return False
    DB_CURSOR.execute("UPDATE Countries SET wiki_data = ?, country_data = ?, timestampe = ? where country_name = ?", ( json.dumps(wiki_data), json.dumps(country_data), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), country_name))
    DB.commit()
    DB.close()
    return True

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

def check_password(username, password):
    return password == get_user(username)[1]
