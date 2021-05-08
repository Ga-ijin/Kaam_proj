# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:34:40 2021

@author: Sarah
"""
import pandas as pd
import os
import numpy as np

# In[1]: Initialisation textes et variables

dir = r'C:\Users\Ga\Documents\GitHub\Kaam_proj'
os.chdir(dir)

text = open('kaam_script_livre1part1_CLEANED.txt', "r", encoding = 'utf-8')
list_ep_txt = open("list_ep.txt", 'r', encoding = 'utf-8')
list_persos = pd.read_csv('list_persos.csv', sep=";", encoding = 'utf-8')

dfEpisodes = pd.DataFrame()
dfPersos = pd.DataFrame()
list_ep = []
list_persos=[]
list_script =[]
perso = ""
cpt_ep = 0
numLivre = 1
txt_modif = text.read()
temp = []
list_sep = []

# In[2]: Initialisation des df des épisodes et des personnages

for line in list_ep_txt:
    cpt_ep+=1
    tuple_ep = (numLivre, cpt_ep, line.strip())
    list_ep.append(tuple_ep)

dfEpisodes = pd.DataFrame(list_ep, columns=['livre', 'num_ep','titre_ep'])

dfPersos = pd.DataFrame(list_persos, columns=['char_id','char_name', 'char_descr', 'knight'])

# In[3]: Séparation des scripts des épisodes
    
for i in dfEpisodes.index:
    titre_ep = dfEpisodes['titre_ep'][i]
    list_sep.append(str(titre_ep) + '\n')

for sep in list_sep:
    temp = txt_modif.split(sep=sep)
    list_script.append(temp[0])
    txt_modif=temp[1]
    
list_script.pop(0)
list_script.append(txt_modif)

dfEpisodes['script'] = list_script

text.close()

nbEp = len(dfEpisodes)
dfEpisodes.insert(0,'ep_id', np.arange(1,nbEp+1))

# In[4]: Création des csv pour backup pour upload dans la base

dfEpisodes.to_csv('csvEpisode_part1.csv', sep=';', index=False, encoding="utf-8")
dfPersos.to_csv('csvPersos.csv', sep=';', index=False, encoding='utf-8')

