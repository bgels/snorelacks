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
        nation = request.form['country'].strip()
        money = request.form['currency'].strip()

        if(not user or not pswd or not money or not nation):
            flash("WARNING: One of the fields cannot be empty!")
            return redirect(url_for('register'))

        # add database registration here
        db.add_user(user, pswd, nation, money)
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
        db_user = db.get_user(user)
        if (db_user is None or not db.check_password(user,pswd)):
            flash("Username or password is not correct!")
            return redirect(url_for('login'))
        flash(f"Login Successful! Welcome back, {user}.")
        session['username'] = user
        return redirect(url_for('profile'))
    return render_template("login.html")
@app.route("/logout", methods=['GET', 'POST'])

def logout():
    session.clear()
    return render_template("homepage.html")

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
    return render_template("profile.html", db_user = db_user)

@app.route("/country", methods=['GET', 'POST'])
def country():
    if request.method == 'POST':
        target_country = request.form['keyword']
        # redirect with reuslts to homepage to render please
        #homepage will then redirect to the right country by calling country
        # make sure to add country to db
    if request.method == 'GET':
        target_country = (request.args.get('keyword') or '').strip()
        try:
            target_country = api.extract_country_name(target_country)
        except:
            flash(f"Invalid country!! please fix to go into a country directory page. Requested country doesn't exist: '{target_country}'?")
            return redirect(url_for('homepage'))
        country_data = []
        if not db.get_country(target_country):
            country_data = api.extract_country_data(target_country)
            actual_name = country_data['country'][0]['name']['common']
            wiki_data = api.extract_wikipedia_subsections(actual_name, "history")
            db.add_country(actual_name, wiki_data, country_data)
            country_data = (actual_name, wiki_data, country_data)
            count_data = country_data[2]
        else:
            country_data = db.get_country(target_country)
            count_data = json.loads(country_data[2])
            wiki_data = json.loads(country_data[1])
    return render_template("country.html", country_data=count_data, wiki_data=wiki_data)

if __name__ == "__main__":
    app.debug = True
    app.run()
