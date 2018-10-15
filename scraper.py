#!/usr/bin/env python3
"""
Scrapes all the property metadata from the results of a daft search.
How to use:
    - Make a normal search on daft.
    - Copy the url in 'URL' below.
    - run script.
"""

import re
import sys
import time
import requests
import bs4


URL = 'https://www.daft.ie/antrim/property-for-sale/?s%5Bmxp%5D=150000'
DOMAIN = 'https://www.daft.ie'


# Looks like daft blocks on certain headers.
HEADERS = {
  'Connection': 'keep-alive',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'en-US,en;q=0.9'
}


BER_REGEX = re.compile(r"^.*ber_(.*).svg$", re.IGNORECASE)
NUMBER_ONLY_REGEX = re.compile(r"[^0-9]", re.IGNORECASE)


# Loop through all result pages
nextUrl = URL
while True:
  response = requests.get(nextUrl, headers=HEADERS)
  text = response.text
  soup = bs4.BeautifulSoup(text, 'html.parser')
  cards = soup.find_all('div', class_ = 'PropertyCardContainer__container')
  print ('got:', len(cards), 'cards', file=sys.stderr)  # log to stderr, results to stdout

  # Loop through each property on the page
  for card in cards:
    urlPath = card.a['href']
    ber = card.find('img', class_ = 'PropertyImage__berImage')
    ber = ber and BER_REGEX.sub(r'\1', ber['src']) or ''
    price = card \
      .find('strong', class_ = 'PropertyInformationCommonStyles__costAmountCopy') \
      .get_text()
    price = NUMBER_ONLY_REGEX.sub('', price)
    delta = card \
      .find('img', class_ = 'PriceIncrease__arrow')
    delta = delta and NUMBER_ONLY_REGEX.sub('', delta.get_text()) or ''
    beds, baths, details = card \
      .find('div', class_ = 'PropertyInformationCommonStyles__quickPropertyDetailsContainer') \
      .get_text() \
      .split(None, 2)
    details = details.strip()
    address = card \
      .find('div', class_ = 'PropertyInformationCommonStyles__addressCopy') \
      .get_text() \
      .strip() \
      .replace('\n', '')
    print (address, price, delta, ber, beds, baths, details, DOMAIN + urlPath, sep='|')
  if not soup.find("a", string="Next"):
    exit(0)
  nextUrl = DOMAIN + soup.find("a", string="Next")['href']
  sys.stdout.flush()
  print ('getting next page:', nextUrl, file=sys.stderr)
