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

print(soup)

print(soup.find("div", { "class" : "info" }))

print(soup.find("div", { "class" : "item_description" }))

print(soup.find("div", { "class" : "list detail eplist" }))

listep = []
for block in soup.find("div", { "class" : "list detail eplist" }):
    listep.append(block)
    
for block in (soup.find("div", { "class" : "list detail eplist" })):
    print(soup.find_all("div", { "class" : "item_description" }, { "itemprop" : "description" }))

for block in soup.find_all("div", { "class" : "item_description" }, { "itemprop" : "description" }):
    print(block.text)



# blocks = soup.select("#content > div:nth-of-type(n+2)")
#     # 2ime boucle sur les block récupérée
# for block in blocks:
#     fact = block.select_one("p")
#     if fact is not None:
#         id = block.select_one("ul.star-rating").attrs['id']
#         #print(id)
#         rate = block.select_one("span.out5Class")
#         vote = block.select_one("span.votesClass")