#!/usr/bin/env python3

import re
import sys

BERS = ['A', 'B', 'C']
BEDS_LIMIT = 3
PRICE_LIMIT = 100000

lines = sys.stdin.readlines()
FORCE_NUMERICAL_REGEX = re.compile(r"[^0-9]", re.IGNORECASE)
for row in lines:
  address, price, delta, ber, beds, baths, _ = row.strip().split('|', 6)
  price = FORCE_NUMERICAL_REGEX.sub('', price)
  beds = FORCE_NUMERICAL_REGEX.sub('', beds)
  if (any(s in ber for s in BERS) and
      int(price) <= PRICE_LIMIT and
      beds.isdigit() and (int(beds) >= BEDS_LIMIT)):
    print (row.strip())

