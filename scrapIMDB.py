# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 15:55:29 2021

@author: Sarah
"""

import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/title/tt0441059/episodes?season=1&ref_=tt_eps_sn_1'

req = requests.get(url)
print(req)
req.text

r = requests.get(url, headers={"User-Agent": "Firefox"})
soup = BeautifulSoup(req.text, 'lxml')

listep = []

for block in soup.find_all("div", { "class" : "item_description" }, { "itemprop" : "description" }):
    print(block.text)