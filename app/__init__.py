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

def extract_country_data(country):
    countries = urlopen(f"https://restcountries.com/v3.1/name/{country}?fields=capital,currencies,languages,name,population,timezones,flag,latlng")
    countries_info = json.load(countries)

    weather_key = open("keys/key_api1.txt")
    weather = urlopen(f"https://api.openweathermap.org/data/2.5/forecast?lat={countries_info[0]['latlng'][0]}&lon={countries_info[0]['latlng'][1]}&units=metric&&appid={weather_key.read()}")
    weather_info = json.load(weather)

    wiki_summary_req = Request(
         url=f"https://en.wikipedia.org/api/rest_v1/page/summary/{country}",
         headers={'User-Agent': 'Mozilla/5.0'}
    )
    wiki_summary = urlopen(wiki_summary_req, timeout=10)
    wiki_summary_info = json.load(wiki_summary)

    places_key = open("keys/key_api2.txt")
    places = urlopen(f"https://api.geoapify.com/v2/places?categories=tourism.attraction&filter=circle:{countries_info[0]['capitalInfo']['latlng'][0]},{countries_info[0]['capitalInfo']['latlng'][1]},5000&limit=20&apiKey={places_key.read()}")
    places_info = json.load(places)

    currencies = []
    for currency in countries_info[0]['currencies']:
        currencies.append(currency)
    exchange_key = open("keys/key_api3.txt")
    exchange_rate = urlopen(f"https://api.exchangerateapi.net/v1/latest?base={user_currency}&currencies={currencies[0]+[','+currencies[i] for i in range(1, len(currrencies))]}&apikey={exchange_key.read()}")
    exchange_info = json.load(exchange_rate)




def extract_wikipedia_subsections(title, section_name):


    sections_req = Request(
            url=f"https://en.wikipedia.org/w/api.php?action=parse&page={title}&prop=sections&format=json",
            headers={'User-Agent': 'Mozilla/5.0'}
    )

    sections = urlopen(wikipedia_req, timeout=10)
    sections_info = json.load(wikipedia)

    section_index = 0

    for section in wikipedia_info['parse']['sections']:
        if section['line'].lower() == section_name.lower():
            section_index = section['index']

    wikipedia_req = Request(
        url=f"https://en.wikipedia.org/w/api.php?action=parse&page={title}&section={section_index}&prop=text&format=json&formatversion=2",
        headers={'User-Agent': 'Mozilla/5.0'}
    )


    soup = BeautifulSoup(wikipedia_info['parse']['text'], 'html.parser')

    section = {}
    h3_tags = soup.find_all('h3')

    for h3 in h3_tags:
        heading = h3.get_text(strip=True)
        pprint.pprint(heading)

        content = ''
        parent = h3.find_parent('div', class_='mw-heading')
        curr = parent.find_next_sibling()

        while curr:
            if curr.name == 'div' and 'mw-heading' in curr.get('class', []):
                break

            if curr.name == 'p':
                text = curr.get_text(strip=False)
                text = re.sub(r'\[\d+\]', ' ', text)
                content += text

            curr = curr.find_next_sibling()

        section[heading] = content

    return section


@app.route("/", methods=['GET', 'POST'])
def index():
    # --- COUNTRIES ----
    countries = urlopen(f"https://restcountries.com/v3.1/name/pakistan?fields=capital,currencies,languages,name,population,timezones,flag,latlng")
    countries_info = json.load(countries)

    # --- WEATHER ---
    weather_key = open("keys/key_api1.txt")
    weather = urlopen(f"https://api.openweathermap.org/data/2.5/forecast?lat={countries_info[0]['latlng'][0]}&lon={countries_info[0]['latlng'][1]}&units=metric&&appid={weather_key.read()}")
    weather_info = json.load(weather)


    #--- WIKIPEDIA SUMMARY ---
    wiki_summary_req = Request(
         url=f"https://en.wikipedia.org/api/rest_v1/page/summary/Pakistan",
         headers={'User-Agent': 'Mozilla/5.0'}
    )
    wiki_summary = urlopen(wiki_summary_req, timeout=10)
    wiki_summary_info = json.load(wiki_summary)
    # pprint.pprint(wiki_summary_info)

    #--- WIKIPEDIA REQUEST TEST ---
    #https://en.wikipedia.org/w/api.php?action=parse&page=Pakistan&prop=sections&format=json
    #https://en.wikipedia.org/w/api.php?action=parse&page=Pakistan&section=41&prop=text&format=json&formatversion=2
    wikipedia_req = Request(
            url=f"https://en.wikipedia.org/w/api.php?action=parse&page=Chad&section=25&prop=text&format=json&formatversion=2",
            headers={'User-Agent': 'Mozilla/5.0'}
    )

    wikipedia = urlopen(wikipedia_req, timeout=10)
    wikipedia_info = json.load(wikipedia)
    # pprint.pprint(wikipedia_info['parse']['text'])

    soup = BeautifulSoup(wikipedia_info['parse']['text'], 'html.parser')

    sections = {}
    h3_tags = soup.find_all('h3')
    for h3 in h3_tags:
        heading = h3.get_text(strip=True)
        pprint.pprint(heading)

        content = ''
        parent = h3.find_parent('div', class_='mw-heading')
        curr = parent.find_next_sibling()

        while curr:
            if curr.name == 'div' and 'mw-heading' in curr.get('class', []):
                break

            if curr.name == 'p':
                text = curr.get_text(strip=False)
                text = re.sub(r'\[\d+\]', ' ', text)
                content += text

            curr = curr.find_next_sibling()

        sections[heading] = content

    # pprint.pprint(sections)




    # print(S.prettify())
    # culture_section_index = None

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
