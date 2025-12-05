#Andrew Tsai, Ricky Lin, Yu Lu, Mustafa Abdullah
#Snorelacks

# Imports
from flask import Flask, render_template, request, flash, url_for, redirect, session
import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O
import os
import urllib.request
import json


# Initialize databases

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)
import pprint

@app.route("/", methods=['GET', 'POST'])
def index():
    
    countries = urllib.request.urlopen(f"https://restcountries.com/v3.1/name/pakistan?fields=capital,currencies,languages,name,population,timezones,flag")

    a = json.load(countries)
    
       
    
    pprint.pprint(a)
    #capital, currency, languages, name, population, timezone, flag for each country,add more later
#name, capital, currency, population, timezone, languages
    
    
    
    return render_template("index.html", name = a[0]["name"]["common"], capital = a[0]["capital"][0], currency = a[0]["currencies"], population = a[0]["population"], timezone = a[0]["timezones"][0])

    

# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     return render_template("index.html")
# 
# @app.route("/homepage", methods=['GET', 'POST'])
# def home():
#     return render_template("index.html")
# 
# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run()

