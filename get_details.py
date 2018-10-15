#!/usr/bin/env python3
"""
Download all the text associated with a single property page.
"""

HEADERS = {
  'Connection': 'keep-alive',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'en-US,en;q=0.9'
}

import re
import sys
import time
import requests
import bs4

lines = sys.stdin.readlines()

for row in lines:
  address, price, delta, ber, beds, baths, details, url = row.strip().split('|')
  response = requests.get(url, headers=HEADERS)
  text = response.text
  soup = bs4.BeautifulSoup(text, 'html.parser')
  pdetails = soup.find('div', class_ = 'PropertyOverview__propertyOverviewDetails')
  if not pdetails:
    continue
  pdetails = re.sub( '\s+', ' ', pdetails.get_text())
  pdescription = soup.find('p', class_ = 'PropertyDescription__propertyDescription')
  pdescription = re.sub( '\s+', ' ', pdescription.get_text())
  print (price, ber, beds, baths, details, url, pdetails, pdescription, sep='|')

