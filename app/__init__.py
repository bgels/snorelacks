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
import os
import api
import re
# Initialize databases

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.context_processor
def user_context(): # persistent info made avalible for all html templates
    return {
        "logged_in": ('username' in session), # eventually change requirement to userid after db is done
        "current_user": session.get('username')
    }

@app.route("/", methods=['GET', 'POST'])
def homepage():
    return render_template("homepage.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username'].strip()
        pswd = request.form['password'].strip()
        nation = None
        money = None

        if(not user or not pswd):
            flash("WARNING: One of the fields cannot be empty!")
            return redirect(url_for('register'))

        # add database registration here
        if db.add_user(user, pswd, nation, money):
            flash(f"Registration Successful! Welcome, {user}. Please log in.")
            return redirect(url_for('login'))
        else:
            flash("Username already exists. Please choose another.")
            return redirect(url_for('register'))
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
        db_user = db.get_user(user)
        if (db_user is None or not db.check_password(user,pswd)):
            flash("Username or password is not correct!")
            return redirect(url_for('login'))
        flash(f"Login Successful! Welcome back, {user}.")
        session['username'] = user
        return redirect(url_for('profile'))
    return render_template("login.html")
@app.route("/logout", methods=['GET', 'POST'])

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('homepage'))

@app.route("/search", methods=['GET', 'POST'])
def search():

    term = (request.args.get('keyword') or '').strip()
    if not term:
        flash("Search: WARNING, no country provided! Listing all existing countries.")
    return render_template("search.html", term = term, results = None)

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    user = session.get('username')
    if (not user):
        flash("You are not logged in!")
        return redirect(url_for('login'))
    db_user = db.get_user(user)
    fav = db.get_favorites(user)
    return render_template("profile.html", db_user = db_user, fav = fav)

@app.route("/country", methods=['GET', 'POST'])
def country():
    if request.method == 'POST':
        target_country = request.form['keyword']
        # redirect with reuslts to homepage to render please
        #homepage will then redirect to the right country by calling country
        # make sure to add country to db
        return redirect(url_for('country', keyword=target_country))
    if request.method == 'GET':
        target_country = (request.args.get('keyword') or '').strip()
        
        if is_ridiculous(target_country): #lol
            flash("No. 🫩")
            flash("Type in a 💔VALID💔 country name 🥀")
            return redirect(url_for('homepage'))
        if not target_country:
            flash(f"Please enter a country name.")
            return redirect(url_for('homepage'))

        db_data = db.get_country(target_country)
        if db_data:
            print(f"Loading {target_country} from database")
            wiki_data = json.loads(db_data[1])
            count_data = json.loads(db_data[2])
            actual_name = api.extract_country_name(target_country)
        else:
            full_country_info = api.extract_country_data(target_country)
            if not full_country_info:
                flash(f"Invalid country: '{target_country}'")
                return redirect(url_for('homepage'))
            actual_name = full_country_info['country'][0]['name']['common']
            wiki_data = api.extract_wikipedia_info(actual_name)
            db.add_country(actual_name, wiki_data, full_country_info)
            count_data = full_country_info
        user = session.get('username')
    return render_template("country.html", favorited = db.country_in_favorites(user, actual_name), country_name = actual_name.replace(" ", "_"), country_data=count_data, wiki_data=wiki_data)

@app.route("/favorite", methods = ['GET', 'POST'])
def favorite_redirect():
    if(db.country_in_favorites(session.get('username'), request.args.get('country').replace("_", " "))):
        db.unfav_country(request.args.get('country').replace("_", " "), session.get('username'))
        print(f"unfav: {request.args.get('country')}, {session.get('username')}")
    else:
        db.fav_country(request.args.get('country').replace("_", " "), session.get('username'))
        print(f"fav: {request.args.get('country')}, {session.get('username')}")
    actual_name = request.args.get('country')
    return redirect(url_for("country", keyword = actual_name.replace("_", " ")))

@app.route("/refresh/<country_name>")
def refresh_country(country_name):
    full_data = api.extract_country_data(country_name)
    
    if not full_data:
        flash("Failed to refresh data. API might be down????")
        return redirect(url_for('country', keyword=country_name))

    actual_name = full_data['country'][0]['name']['common']
    wiki_data = api.extract_wikipedia_info(actual_name)

    db.add_country(actual_name, wiki_data, full_data)
    
    flash(f"Data for {actual_name} has been refreshed!")
    return redirect(url_for('country', keyword=actual_name))

def is_ridiculous(text):
    if re.search(r"[\]\\\[=\-\":><&@*^#@%$]", text):
        return True
    if len(text) > 60:
        return True
    return False
    
if __name__ == "__main__":
    app.debug = True
    app.run()
