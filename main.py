"""

projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Katerina Novakova

email: katule.novakova@email.cz

discord: katysb5#4067

"""

from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
import requests
import re
import csv
import sys
import os


if len(sys.argv) != 3:
        print("Incorrect arguments.")
        exit(1)

url = sys.argv[1]
file = sys.argv[2]
split_up = os.path.splitext(file)
split_text = split_up[0]
split_ext = split_up[1]
if split_ext != ".csv":
        print("Incorrect file, must have csv extension.")
        exit(1)

try:
    response = requests.get(url)
    response.raise_for_status()
except HTTPError as hp:
    print(hp)
    print("Invalid url adress.")
    exit(1)

html_text = requests.get(url).text
html_base = 'https://volby.cz/pls/ps2017nss/'
if html_base not in url:
        print("Incorrect url adress.")
        exit(1)

soup = BeautifulSoup(html_text, 'lxml')
tables = soup.find_all('table', class_ = 'table')
csv_file = open(file, mode='w', encoding= "UTF8")
writer_tool = csv.writer(csv_file, delimiter= ";", lineterminator= "\n")
first_row = ["code", "location", "registered", "envelopes", "valid"]

# getting the names of the parties for the first row
table = soup.find('table', class_ = 'table')
lines = table.find_all('tr')
html_addon = (lines[2].find('a', href = True).get('href'))
next_html = html_base + html_addon
next_html_text = requests.get(next_html).text
next_soup = BeautifulSoup(next_html_text, 'lxml')
party_tables = next_soup.find_all('div', class_ = 't2_470')
party_name = []
for party_table in party_tables:
        lines = party_table.find_all('tr')
        for i, line in enumerate(lines):
                if i < 2:
                        continue
                tmp = line.find('td', class_ = 'overflow_name', headers = re.compile('t[1|2]sa1 t[1|2]sb2'))
                if tmp is not None:
                        party_name.append(tmp.text)

# headers of the file
first_row.extend(party_name)
writer_tool.writerow(first_row)

# getting the data for each location and party
for table in tables:
        lines = table.find_all('tr')

        for i, line in enumerate(lines):
                registred = 0
                envelopes = 0
                valid = 0
                total = []
                next_row = []
                if i < 2:
                        continue
                town = line.find('td', class_ = 'cislo')
                if (town is None):
                        continue
                town = line.find('td', class_ = 'cislo').text
                next_row.append(town)
                name = line.find('td', class_ = 'overflow_name').text
                next_row.append(name)
                html_addon = (line.find('a', href = True).get('href'))
                next_html = html_base + html_addon
                next_html_text = requests.get(next_html).text
                next_soup = BeautifulSoup(next_html_text, 'lxml')
                registred = next_soup.find('td', class_ = 'cislo', headers = 'sa2').text
                next_row.append(registred)
                envelopes = next_soup.find('td', class_ = 'cislo', headers = 'sa3').text
                next_row.append(envelopes)
                valid = next_soup.find('td', class_ = 'cislo', headers = 'sa6').text
                next_row.append(valid)
                party_tables = next_soup.find_all('div', class_ = 't2_470')

                for party_table in party_tables:
                        lines_j = party_table.find_all('tr')
                        for j, line_j in enumerate(lines_j):
                                if j < 2:
                                        continue
                                tmp = line_j.find('td', class_ = 'cislo', headers = re.compile('t[1|2]sa2 t[1|2]sb3'))
                                if tmp is not None:
                                        total.append("".join(tmp.text.split()))

                # writting each row with data
                next_row.extend(total)
                writer_tool.writerow(next_row)

csv_file.close()


