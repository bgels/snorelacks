from flask import Flask, render_template, request, flash, url_for, redirect, session
import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O
import os
from urllib.request import Request, urlopen
import urllib.parse
import re
import json
import pprint
from bs4 import BeautifulSoup


def extract_country_data(country):
    try:
        country_data = {}
        user_currency = "USD"
        fields = "fields=capital,currencies,languages,name,population,timezones,flags,latlng,capitalInfo,region"
        country = urllib.parse.quote(country)
        try:
            countries = urlopen(f"https://restcountries.com/v3.1/name/{country}?{fields}")
            countries_info = json.load(countries)
        except:
            countries = urlopen(f"https://restcountries.com/v3.1/alpha/{country}?{fields}")
            countries_info = json.load(countries)
        
        country_data["country"] = countries_info
    except Exception as e:
        print(f"Could not find country '{country}': {e}")
        return None

    # region
    try:
        raw_region = countries_info[0].get('region', 'Unknown')
        country_data['region_display'] = raw_region
        if raw_region in ['Europe', 'Africa']:
            country_data['font_group'] = "font-emea"
        elif raw_region == 'Americas':
            country_data['font_group'] = "font-americas"
        elif raw_region in ['Asia', 'Oceania']:
            country_data['font_group'] = "font-asia"
        else:
            country_data['font_group'] = "font-americas"
    except:
        country_data['region_display'] = ""
        country_data['font_group'] = ""

    # capital img (Wikipedia)
    try:
        capital = countries_info[0]['capital'][0]
        country_data['capital'] = capital
        encoded_capital = urllib.parse.quote(capital)
        capital_req = Request(
            url=f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_capital}",
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        capital_data = json.load(urlopen(capital_req, timeout=5))
        country_data["capital_image"] = capital_data.get('originalimage', {}).get('source')
    except Exception as e:
        print(f"Capital Image failed: {e}")
        country_data["capital_image"] = None

    # weather
    try:
        weather_key = open("keys/key_api1.txt").read().strip()
        lat = countries_info[0]['latlng'][0]
        lon = countries_info[0]['latlng'][1]
        weather = urlopen(f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={weather_key}")
        country_data["weather"] = json.load(weather)
    except Exception as e:
        print(f"Weather failed: {e}")
        country_data["weather"] = None

    # wiki
    try:
        common_name = countries_info[0]['name']['common']
        wiki_summary_req = Request(
             url=f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(common_name)}",
             headers={'User-Agent': 'Mozilla/5.0'}
        )
        country_data["summary"] = json.load(urlopen(wiki_summary_req, timeout=10))
    except Exception as e:
        print(f"Wiki Summary failed: {e}")
        country_data["summary"] = {'extract_html': 'No summary available.', 'thumbnail': None}

    #places (Geoapify)
    try:
        places_key = open("keys/key_api2.txt").read().strip()
        cap_lat = countries_info[0]['capitalInfo']['latlng'][0]
        cap_lon = countries_info[0]['capitalInfo']['latlng'][1]
        places = urlopen(f"https://api.geoapify.com/v2/places?categories=tourism.attraction&filter=circle:{cap_lat},{cap_lon},5000&limit=20&apiKey={places_key}")
        country_data["places"] = json.load(places)
    except Exception as e:
        print(f"Places API failed: {e}")
        country_data["places"] = None

    #currency
    try:
        currencies = list(countries_info[0]['currencies'].keys())
        currency_list = ",".join(currencies)
        exchange_key = open("keys/key_api3.txt").read().strip()
        exchange_rate = urlopen(f"https://api.exchangerateapi.net/v1/latest?base={user_currency}&currencies={currency_list}&apikey={exchange_key}")
        country_data["currency"] = json.load(exchange_rate)
    except Exception as e:
        print(f"Currency API failed: {e}")
        country_data["currency"] = None

    return country_data



def extract_wikipedia_subsections(title, section_name):
    try:
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
    except:
        return None

if __name__ == "__main__":
    pprint.pprint(extract_country_data("Pakistan"))
    pprint.pprint(extract_country_data("Narnia"))
    pprint.pprint(extract_wikipedia_subsections("The Chronicles of Narnia", "Culture"))
