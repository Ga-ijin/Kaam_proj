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
dfEpComment['rea'] = ""
dfEpComment['scenar'] = ""

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
        dfEpComment.loc[cptDf, 'rea'] = (rea.findNext('div').text)
        
    scenar = div.find("b", text="Scénario")
    if scenar:
        dfEpComment.loc[cptDf, 'scenar'] = (scenar.findNext('div').text)
        
    resume = div.find("b", text="Résumé détaillé")
    if resume:
        dfEpComment.loc[cptDf, 'resume_vf'] = (resume.findNext('div').text)
    cptDf+=1

# Retrait des sauts de ligne
def stripping(case):
    case = case.replace("\n", " ").strip('"')
    return case

dfEpComment["resume_vf"] = dfEpComment["resume_vf"].apply(stripping)

# In[7]: Création des csv pour backup pour upload dans la base
    
#Table episode [suite] sur base du csv partiellement rempli

dfEpisodes = pd.read_csv('rawData/csvEpisode_part0.csv', sep=';')
dfFinal = dfEpisodes.join(dfEpComment, how='inner')
dfTableEp = dfFinal[["ep_id","livre","num_ep","titre_ep","script","resume_vf","resume_va"]]

dfTableEp["script"] = dfTableEp["script"].apply(stripping)
dfTableEp.to_csv('csvImportData/csvEpisode2.csv', sep=';', encoding='utf-8', index=False)
dfTableRating = dfFinal[["ep_id","rating","nb_votes"]]

dfTableRating.to_csv('csvImportData/csvRating2.csv', sep=';', encoding='utf-8', index=False)

# In[8]: Qui est réalisateur ? Scénariste ?

liste_reals = list(dfEpComment["rea"].apply(lambda x : x.strip("\n")).unique())
liste_scena = list(dfEpComment["scenar"].apply(lambda x : x.strip("\n")).unique())

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

liste_reals_firstname = [i.split(' ')[0] for i in liste_reals] 
liste_reals_lastname = [i.split(' ', maxsplit=1)[1] for i in liste_reals] 
liste_scenas_firstname = [i.split(' ')[0] for i in liste_scena] 
liste_scenas_lastname = [i.split(' ', maxsplit=1)[1] for i in liste_scena] 

dataDictRea = {'rea_firstname':pd.Series(liste_reals_firstname), 'rea_lastname':pd.Series(liste_reals_lastname)}
dfCheckRea = pd.DataFrame(dataDictRea)
dataDictScenar = {'scenar_firstname':pd.Series(liste_scenas_firstname), 'scenar_lastname':pd.Series(liste_scenas_lastname)}
dfCheckScenar = pd.DataFrame(dataDictScenar)

df_people = pd.read_csv("csvImportData/csvPeople.csv", sep=";")
df_people['people_id']=range(1, len(df_people)+1)


dfCrew = pd.DataFrame(range(1, len(dfEpisodes)+1), columns=["ep_id"])
dfTemp = pd.DataFrame(liste_scena, columns=["people_id"])
dfCrew['key'] = 0
dfTemp['key'] = 0
dfCrew = dfCrew.merge(dfTemp, on="key", how="outer").drop("key", axis=1)

dfCrew["is_rea"] = False
dfCrew["is_scenar"] = False


for i in range(len(dfCrew)) :
    dfCrew.at[i,"is_rea"] =  dfCrew.at[i,"people_id"] in dfEpComment.at[dfCrew.at[i,"ep_id"]-1,"rea"]
    dfCrew.at[i,"is_scenar"] =  dfCrew.at[i,"people_id"] in dfEpComment.at[dfCrew.at[i,"ep_id"]-1,"scenar"]

dfFinal = pd.DataFrame(columns=["ep_id",'people_id','is_rea','is_scenar'])
for i in range(len(dfCrew)) :
    if (dfCrew.at[i,'is_rea'] == False) & (dfCrew.at[i,'is_scenar'] == False):
        dfCrew = dfCrew.drop([i])

df_people['checkName'] = df_people['people_firstname'] + ' ' + df_people['people_lastname']

dicIdRea = {df_people.loc[df_people['checkName'].isin(liste_reals)]['checkName'].iat[0] : 
            df_people.loc[df_people['checkName'].isin(liste_reals)]['people_id'].iat[0]}
    
for key in dicIdRea:
    dfCrew['people_id'][dfCrew['people_id']== key] = dicIdRea[key]

dicIdScenar = {}
for i in range(len(liste_scena)):
    dicIdScenar[ df_people.loc[df_people['checkName'].isin(liste_scena)]['checkName'].iat[i] ] = df_people.loc[df_people['checkName'].isin(liste_scena)]['people_id'].iat[i]

for key in dicIdScenar:
    dfCrew['people_id'][dfCrew['people_id']== key] = dicIdScenar[key]
    
dfCrew.to_csv('csvImportData/csvCrew2.csv', sep=';', encoding='utf-8', index=False)