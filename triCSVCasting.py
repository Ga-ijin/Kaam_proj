# -*- coding: utf-8 -*-
"""
Created on Fri May  7 11:10:48 2021

@author: Ga
"""

import pandas as pd
from itertools import compress
import os

dir = r'C:\Users\Ga\Documents\GitHub\Kaam_proj\csvImportData'
os.chdir(dir)

dfChara = pd.read_csv("csvCharacters.csv", sep=";")

dfEp = pd.read_csv("csvEpisode2.csv", sep=";" )

dfEp["liste_persos"] = 0
dfEp["liste_persos"] = dfEp["liste_persos"].astype(object)


list_per = dfChara.loc[:,"char_name"]

for i in range(len(dfEp)) : 
    boolist=[]
    for nom in list_per : 
       boolist.append(nom in dfEp.loc[i,"script"])
    dfEp.at[i,"liste_persos"] = list(compress(list_per,boolist))

df_ex = dfEp.explode("liste_persos")

df_final = df_ex[["ep_id","liste_persos"]]

df_final = df_final.merge(dfChara, how ='left', left_on = 'liste_persos', right_on = 'char_name')
df_final = df_final[['ep_id','char_id']]

df_final.to_csv('csvCasting2.csv', sep=';', encoding='utf-8', index=False)
