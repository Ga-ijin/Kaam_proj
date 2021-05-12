# -*- coding: utf-8 -*-
"""
Created on Wed May 12 10:08:04 2021

@author: Ga
"""
import pandas as pd
import os

dir = r'C:\Users\Ga\Documents\GitHub\Kaam_proj'
os.chdir(dir)


with open('rawData/persos.txt', 'r', encoding='utf-8') as file:
    data=file.readlines()
    
for i in range(len(data)):
    if ',' not in data[i]:
        data[i] = data[i] + ", "

charName = [i.split(',')[0] for i in data] 
charName = [i.upper() for i in charName]
charName = [i.strip('\n') for i in charName]
charDescr = [i.split(',')[1] for i in data]
charDescr = [i.strip() for i in charDescr]
charDescr = [i.capitalize() for i in charDescr]
isKnight=[]

for line in charName:
    if '†' in line:
        isKnight.append('True')
    else: isKnight.append('False')

charName = [i.split(' †')[0] for i in charName]

dataDict = {"char_name": pd.Series(charName), 'char_descr':pd.Series(charDescr), 'knight':pd.Series(isKnight)}

dfPerso = pd.DataFrame(dataDict)
