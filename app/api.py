from flask import Flask, render_template, request, flash, url_for, redirect, session
import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O
import os
from urllib.request import Request, urlopen
import re
import json
import pprint
from bs4 import BeautifulSoup


def extract_country_data(country):
    country_data = {}
    user_currency = "USD"

    countries = urlopen(f"https://restcountries.com/v3.1/name/{country}?fields=capital,currencies,languages,name,population,timezones,flag,latlng,capitalInfo")
    countries_info = json.load(countries)
    country_data["country"] = countries_info

    weather_key = open("keys/key_api1.txt")
    weather = urlopen(f"https://api.openweathermap.org/data/2.5/forecast?lat={countries_info[0]['latlng'][0]}&lon={countries_info[0]['latlng'][1]}&units=metric&&appid={weather_key.read()}")
    weather_info = json.load(weather)
    country_data["weather"] = weather_info

    wiki_summary_req = Request(
         url=f"https://en.wikipedia.org/api/rest_v1/page/summary/{country}",
         headers={'User-Agent': 'Mozilla/5.0'}
    )
    wiki_summary = urlopen(wiki_summary_req, timeout=10)
    wiki_summary_info = json.load(wiki_summary)
    country_data["summary"] = wiki_summary_info

    places_key = open("keys/key_api2.txt")
    places = urlopen(f"https://api.geoapify.com/v2/places?categories=tourism.attraction&filter=circle:{countries_info[0]['capitalInfo']['latlng'][0]},{countries_info[0]['capitalInfo']['latlng'][1]},5000&limit=20&apiKey={places_key.read()}")
    places_info = json.load(places)
    country_data["places"] = places_info

    currencies = list(countries_info[0]['currencies'].keys())
    currency_list = ",".join(currencies)

    exchange_key = open("keys/key_api3.txt")
    exchange_rate = urlopen(f"https://api.exchangerateapi.net/v1/latest?base={user_currency}&currencies={currency_list}&apikey={exchange_key.read()}")
    exchange_info = json.load(exchange_rate)
    country_data["currency"] = exchange_info

    return country_data



def extract_wikipedia_subsections(title, section_name):

    sections_req = Request(
            url=f"https://en.wikipedia.org/w/api.php?action=parse&page={title}&prop=sections&format=json",
            headers={'User-Agent': 'Mozilla/5.0'}
    )

    sections = urlopen(sections_req, timeout=10)
    sections_info = json.load(sections)

    section_index = 0

    for section in sections_info['parse']['sections']:
        if section['line'].lower() == section_name.lower():
            section_index = section['index']

    wikipedia_req = Request(
        url=f"https://en.wikipedia.org/w/api.php?action=parse&page={title}&section={section_index}&prop=text&format=json&formatversion=2",
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    wikipedia = urlopen(wikipedia_req, timeout=10)
    wikipedia_info = json.load(wikipedia)


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

pprint.pprint(extract_country_data("Pakistan"))
pprint.pprint(extract_wikipedia_subsections("Pakistan", "Culture"))
