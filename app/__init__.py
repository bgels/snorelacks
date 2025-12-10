#Andrew Tsai, Ricky Lin, Yu Lu, Mustafa Abdullah
#Snorelacks

# Imports
from flask import Flask, render_template, request, flash, url_for, redirect, session
import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O
import os
from urllib.request import Request, urlopen
import re
import json
import pprint
from bs4 import BeautifulSoup


# Initialize databases

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)

def extract_wikipedia_subsections(title, section_name):
    wikipeda_req = Request(
            url=f"https://en.wikipedia.org/api/rest_v1/page/mobile-html/{title}",
            headers={'User-Agent': 'Mozilla/5.0'}
    )

    wikipeda = urlopen(wikipedia_req, timeout=10)
    wikipedia_info = json.load(wikipedia)
    
    S = BeautifulSoup("https://en.wikipedia.org/api/rest_v1/page/mobile-html/Pakistan", 'lxml')
        
    
 
    pass

@app.route("/", methods=['GET', 'POST'])
def index():
    countries = urlopen(f"https://restcountries.com/v3.1/name/pakistan?fields=capital,currencies,languages,name,population,timezones,flag,latlng")
    countries_info = json.load(countries)

    weather_key = open("keys/key_api1.txt")
    weather = urlopen(f"https://api.openweathermap.org/data/2.5/forecast?lat={countries_info[0]['latlng'][0]}&lon={countries_info[0]['latlng'][1]}&units=metric&&appid={weather_key.read()}")
    weather_info = json.load(weather)
    #https://en.wikipedia.org/w/api.php?action=parse&page=Pakistan&prop=sections&format=json
    #https://en.wikipedia.org/w/api.php?action=parse&page=Pakistan&section=41&prop=text&format=json&formatversion=2

    wiki_summary_req = Request(
         url=f"https://en.wikipedia.org/api/rest_v1/page/summary/Pakistan",
         headers={'User-Agent': 'Mozilla/5.0'}
    )
    wiki_summary = urlopen(wiki_summary_req, timeout=10)
    wiki_summary_info = json.load(wiki_summary)
   
#    wikipedia_req = Request(
#        url=f"https://en.wikipedia.org/w/api.php?action=parse&page=Pakistan&section=41&prop=text&format=json&formatversion=2",
#        headers={'User-Agent': 'Mozilla/5.0'}
#    ) 
#    wikipedia = urlopen(wikipedia_req, timeout=10)
#    wikipedia_info = json.load(wikipedia)
#    pprint.pprint(wiki_summary_info['extract'])
    culture_section_index = None
    
#    places_key = open("keys/key_api2.txt")
#    places = urlopen(f"https://")
#    places_info = json.load(places)
#
#    exchange_key = open("keys/key_api3.txt")
#    exchange_rate = urlopen(f"")
    



    
    # pprint.pprint(wikipedia_info)  
    #pprint.pprint(countries_info)
    #pprint.pprint(weather_info)
    #capital, currency, languages, name, population, timezone, flag for each country,add more later
#name, capital, currency, population, timezone, languages
    
    
    
    return render_template("index.html", 
        name = countries_info[0]["name"]["common"], capital = countries_info[0]["capital"][0], currency = countries_info[0]["currencies"], population = countries_info[0]["population"], timezone = countries_info[0]["timezones"][0]
    )

    

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


