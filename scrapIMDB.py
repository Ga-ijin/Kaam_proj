# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 15:55:29 2021

@author: Sarah
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np

# In[0]: Requête Beautiful Soup

url = 'https://www.imdb.com/title/tt0441059/episodes?season=1&ref_=tt_eps_sn_1'

req = requests.get(url)
print(req)

r = requests.get(url, headers={"User-Agent": "Firefox"})
soup = BeautifulSoup(req.text, 'lxml')

# In[1]: Initialisation des variables

rate = []
rateClean = []
nbVotes = []
nbVotesClean = []
epDesc = []
epDescClean = []

# In[2]: Récupération de la note par épisode

for block in soup.find_all("span", { "class" : "ipl-rating-star__rating" }):
    rate.append(block.text)
# Conversion en float
for i in range(0, len(rate), 23):
    rateClean.append(float(rate[i]))

# In[3]: Récupération du nombre de votes par épisode
for block in soup.find_all("span", { "class" : "ipl-rating-star__total-votes" }):
    nbVotes.append(block.text)

# Retrait des parenthèses et conversion en int
for el in nbVotes:
    nbVotesClean.append(int((re.sub('[()]', '', el))))

# In[4]: Récupération du résumé des épisodes en VA sur IMDb
for block in soup.find_all("div", { "class" : "item_description", "itemprop":"description"}):
    epDesc.append(block.text)
    
# Nettoyage : retrait des espaces et sauts de ligne, vide si pas de description disponible
for el in epDesc:
    cleanLine = el.strip('\t')
    cleanLine = cleanLine.strip('\n')
    if("Know what this is about?" in el):
        cleanLine = ""
    else:
        cleanLine = cleanLine[4:]
    epDescClean.append(cleanLine)
    
# In[5]: Création du df contenant l'ensemble

dfEpComment = pd.DataFrame(rateClean, columns=['Note'])
dfEpComment['NbVotes'] = nbVotesClean
dfEpComment['Resume Episode VA'] = epDescClean
dfEpComment['Resume Episode VF'] = np.nan
dfEpComment['Realisation'] = np.nan
dfEpComment['Scenario'] = np.nan
# del dfEpComment

# In[6]: Récupération du résumé des épisodes en VF sur Wikipedia

url = 'https://fr.wikipedia.org/wiki/Saison_1_de_Kaamelott'

req = requests.get(url)
print(req)

r = requests.get(url, headers={"User-Agent": "Firefox"})
soup = BeautifulSoup(req.text, 'lxml')

listDiv = []
listCheck = []
cptDf = 0

for div in soup.find_all('div'):
    listDiv.append(div.text)


for i in range(len(listDiv)):
    if("Numéro de production" in listDiv[i]):
        tuple_ep = (listDiv[i+3], listDiv[i+4], listDiv[i+5])
        listCheck.append(tuple_ep)

for i in range(len(listDiv)):
    if("Numéro de production" in listDiv[i]):
        # tuple_ep = (listDiv[i+3], listDiv[i+4], listDiv[i+5])
        
        dfEpComment.loc[cptDf, 'Realisation'] = listDiv[i+3]
        dfEpComment.loc[cptDf, 'Scenario'] = listDiv[i+4]
        dfEpComment.loc[cptDf, 'Resume Episode VF'] = listDiv[i+5]
        cptDf+=1