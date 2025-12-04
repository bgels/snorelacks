#Andrew Tsai, Ricky Lin, Yu Lu, Mustafa Abdullah
#Snorelacks

# Imports
from flask import Flask, render_template, request, flash, url_for, redirect, session
import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

import entries, auth

# Initialize databases

app = Flask(__name__)
app.secret_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")




if __name__ == "__main__":
    app.debug = True
    app.run()
