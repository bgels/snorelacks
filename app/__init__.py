#Andrew Tsai, Ricky Lin, Yu Lu, Mustafa Abdullah
#Snorelacks

# Imports
from flask import Flask, render_template, request, flash, url_for, redirect, session
import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O


# Initialize databases

app = Flask(__name__)
app.secret_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"


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
        # maybe country too? for now just username and password

        if(not user or not pswd):
            flash("WARNING: Username and Password cannot be empty!")
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
