# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:34:40 2021

@author: Sarah
"""
import pandas as pd

# In[1]: Initialisation textes et variables

text = open("kaam_script_livre1part1_CLEANED.txt", "r", encoding = 'utf-8')
list_ep_txt = open("list_ep.txt", 'r', encoding = 'utf-8')
list_persos_xlsx = pd.read_excel('list_persos.xlsx', encoding = 'utf-8')

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

dfEpisodes = pd.DataFrame(list_ep, columns=['livre', 'num_ep','titre'])

dfPersos = pd.DataFrame(list_persos_xlsx, columns=['personnage', 'description', 'chevalier'])

# In[3]: Séparation des scripts des épisodes
    
for i in dfEpisodes.index:
    titre_ep = dfEpisodes['titre'][i]
    list_sep.append(str(titre_ep) + '\n')

for sep in list_sep:
    temp = txt_modif.split(sep=sep)
    list_script.append(temp[0])
    txt_modif=temp[1]
    
list_script.pop(0)
list_script.append(txt_modif)

dfEpisodes['script'] = list_script

# Scrapper les notes des épisodes sur imDB et les stocker dans une colonne

# Réaliser le workbench de la bdd

# Uploader le df dans la BDD

text.close()
