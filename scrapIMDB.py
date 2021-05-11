# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 15:55:29 2021

@author: Sarah
"""

# In[0]: Initialisation textes et variables

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os

dir = r'C:\Users\Ga\Documents\GitHub\Kaam_proj'
os.chdir(dir)

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

dfEpComment = pd.DataFrame(rateClean, columns=['rating'])
dfEpComment['nb_votes'] = nbVotesClean
dfEpComment['resume_va'] = epDescClean
dfEpComment['resume_vf'] = ""
dfEpComment['Realisation'] = ""
dfEpComment['Scenario'] = ""
# del dfEpComment

# In[6]: Récupération du résumé des épisodes en VF sur Wikipedia

url = 'https://fr.wikipedia.org/wiki/Saison_1_de_Kaamelott'

req = requests.get(url)
print(req)

r = requests.get(url, headers={"User-Agent": "Firefox"})
soup = BeautifulSoup(req.text, 'lxml')

cptDf = 0

# On stocke toutes les div contenant les informations pour chaque épisode dans une liste
divs = soup.find_all('div', attrs={'style': 'background-color:#FFFFFF;padding: 5px 10px 0px 15px'})

# Dans cette liste, on recherche les réalisateur(s), scénariste(s) et résumé de chaque bloc
for div in divs:
    rea = div.find("b", text="Réalisation")
    if rea:
        dfEpComment.loc[cptDf, 'Realisation'] = (rea.findNext('div').text)
        
    scenar = div.find("b", text="Scénario")
    if scenar:
        dfEpComment.loc[cptDf, 'Scenario'] = (scenar.findNext('div').text)
        
    resume = div.find("b", text="Résumé détaillé")
    if resume:
        dfEpComment.loc[cptDf, 'resume_vf'] = (resume.findNext('div').text)
    cptDf+=1

def stripping(case):
    case = case.replace("\n", " ").strip('"')
    return case

dfEpComment["resume_vf"] = dfEpComment["resume_vf"].apply(stripping)

# In[7]: Création des csv pour backup pour upload dans la base
    
#Table episode [suite] sur base du csv partiellement rempli

dfEpisodes = pd.read_csv('csvEpisode_part1.csv', sep=';')
dfFinal = dfEpisodes.join(dfEpComment, how='inner')
dfTableEp = dfFinal[["ep_id","livre","num_ep","titre_ep","script","resume_vf","resume_va"]]

dfTableEp["script"] = dfTableEp["script"].apply(stripping)
dfTableRating = dfFinal[["ep_id","rating","nb_votes"]]

dfTableRating.to_csv('csvRating.csv', sep=';', encoding='utf-8', index=False)
# dfTableEp.to_csv('csvEpisode.csv', sep=';', encoding='utf-8', index=False, header=False)

# In[8]: Création des listes de réal

liste_reals = list(dfEpComment["Realisation"].apply(lambda x : x.strip("\n")).unique())
liste_scena = list(dfEpComment["Scenario"].apply(lambda x : x.strip("\n")).unique())

for item in liste_scena : 
    if "-" in item : 
        temp = item.split(" - ")
        liste_scena.extend(temp)
        liste_scena.remove(item)
      
liste_scena = list(set(liste_scena))

for item in liste_reals : 
    if "-" in item : 
        temp = item.split(" - ")
        liste_reals.extend(temp)
        liste_reals.remove(item)
        
liste_reals = list(set(liste_reals))

df_people = pd.read_csv("csvPeople.csv", sep=";")
df_people["is_rea"] = False
df_people["is_scenar"] = False

for i in range(len(df_people)):
    nom = df_people.loc[i, 'people_firstname']+ " " + df_people.loc[i,'people_lastname']
    if nom in liste_reals:
        df_people.loc[i,'is_rea'] = True
    if nom in liste_scena:
        df_people.loc[i,'is_scenar'] = True

