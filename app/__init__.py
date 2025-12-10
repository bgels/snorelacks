#Andrew Tsai, Ricky Lin, Yu Lu, Mustafa Abdullah
#Snorelacks

# Imports
from flask import Flask, render_template, request, flash, url_for, redirect, session
import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O
import db
import json
from urllib.request import Request, urlopen
import pprint

# Initialize databases

app = Flask(__name__)
app.secret_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"

def api_content():
    countries = urlopen(f"https://restcountries.com/v3.1/name/pakistan?fields=capital,currencies,languages,name,population,timezones,flag,latlng,capitalInfo")
    countries_info = json.load(countries)

    weather_key = open("keys/key_api1.txt")
    weather = urlopen(f"https://api.openweathermap.org/data/2.5/forecast?lat={countries_info[0]['latlng'][0]}&lon={countries_info[0]['latlng'][1]}&units=metric&&appid={weather_key.read()}")
    weather_info = json.load(weather)
    #https://en.wikipedia.org/w/api.php?action=parse&page=Pakistan&prop=sections&format=json
    wikipedia_req = Request(
        url=f"https://en.wikipedia.org/w/api.php?action=parse&page=Pakistan&section=41&prop=text&format=json&formatversion=2",
        headers={'User-Agent': 'Mozilla/5.0'}
    ) 
    wikipedia = urlopen(wikipedia_req, timeout=10)
    wikipedia_info = json.load(wikipedia)
    wikipedia_html = wikipedia_info['parse']['text']
    # pprint.pprint(wikipedia_html)
    culture_section_index = None
    
    places_key = open("keys/key_api2.txt")
    places = urlopen(f"https://api.geoapify.com/v2/places?categories=tourism.attraction&filter=circle:{countries_info[0]['capitalInfo']['latlng'][0]},{countries_info[0]['capitalInfo']['latlng'][1]},5000&limit=20&apiKey={places_key.read()}")
    places_info = json.load(places)

    exchange_key = open("keys/key_api3.txt")
    exchange_rate = urlopen(f"https://api.exchangerateapi.net/v1/latest?base=USD&currencies=PKR&apikey={exchange_key.read()}")
    exchange_info = json.load(exchange_rate)
    
    # pprint.pprint(wikipedia_info)  
    #pprint.pprint(countries_info)
    #pprint.pprint(weather_info)
    #pprint.pprint(exchange_info)
    #capital, currency, languages, name, population, timezone, flag for each country,add more later
#name, capital, currency, population, timezone, languages
    # return render_template("index.html", 
    #     name = countries_info[0]["name"]["common"], capital = countries_info[0]["capital"][0], currency = countries_info[0]["currencies"], population = countries_info[0]["population"], timezone = countries_info[0]["timezones"][0]
    # )

@app.context_processor
def user_context(): # persistent info made avalible for all html templates
    return {
        "logged_in": ('username' in session), # eventually change requirement to userid after db is done
        "current_user": session.get('username')
    }

@app.route("/", methods=['GET', 'POST'])
def homepage():
    flash("Welcome to Snorelacks!Welcome to Snorelacks!Welcome to Snorelacks!Welcome to Snorelacks!Welcome to Snorelacks!")
    return render_template("homepage.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username'].strip()
        pswd = request.form['password'].strip()
        nation = request.form['country'].strip()
        money = request.form['currency'].strip()
        db.add_user(user, pswd, nation, money)

        if(not user or not pswd or not money or not nation):
            flash("WARNING: One of the fields cannot be empty!")
            return redirect(url_for('register'))

        # add database registration here
        flash(f"Registration Successful! Welcome, {user}. Please log in.")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username'].strip()
        pswd = request.form['password'].strip()
        if(not user or not pswd):
            flash("WARNING: Username and Password cannot be empty!")
            return redirect(url_for('login'))

        # add database authentication here
        flash(f"Login Successful! Welcome back, {user}.")
        return redirect(url_for('profile'))
    return render_template("login.html")
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template("homepage.html")
@app.route("/user_profile", methods=['GET', 'POST'])
def user_profile():
    #checks session for logged in
    #else won't render profile widgets in template
    return render_template("profile.html")

@app.route("/search", methods=['GET', 'POST'])
def search():
    term = (request.args.get('keyword') or '').strip()
    if not term:
        flash("Search: WARNING, no country provided! Listing all existing countries.")

    # database search logic would go here eventually
    # results = entries.search(term)
    # if not results:
    #     flash(f"Search: No posts found for '{term}'.")

    return render_template("search.html", term = term, results = None)

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    return render_template("profile.html")

@app.route("/country", methods=['GET', 'POST'])
def country():
    return render_template("country.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
