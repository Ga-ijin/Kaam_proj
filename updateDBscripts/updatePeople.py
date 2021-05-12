# -*- coding: utf-8 -*-
"""
Created on Wed May 12 15:30:13 2021

@author: Ga
"""

# Voir scrapIMDB pour requêter les réa/scénaristes des épisodes concernés

# Une fois le df scrappé sur IMDB, vérification des valeurs uniques de nom
# liste_reals = list(dfEpComment["rea"].apply(lambda x : x.strip("\n")).unique())
# liste_scena = list(dfEpComment["scenar"].apply(lambda x : x.strip("\n")).unique())

# for item in liste_scena : 
#     if "-" in item : 
#         temp = item.split(" - ")
#         liste_scena.extend(temp)
#         liste_scena.remove(item)
      
# liste_scena = list(set(liste_scena))

# for item in liste_reals : 
#     if "-" in item : 
#         temp = item.split(" - ")
#         liste_reals.extend(temp)
#         liste_reals.remove(item)
        
# liste_reals = list(set(liste_reals))

# liste_reals_firstname = [i.split(' ')[0] for i in liste_reals] 
# liste_reals_lastname = [i.split(' ', maxsplit=1)[1] for i in liste_reals] 
# liste_scenas_firstname = [i.split(' ')[0] for i in liste_scena] 
# liste_scenas_lastname = [i.split(' ', maxsplit=1)[1] for i in liste_scena] 

# dataDictRea = {'rea_firstname':pd.Series(liste_reals_firstname), 'rea_lastname':pd.Series(liste_reals_lastname)}
# dfCheckRea = pd.DataFrame(dataDictRea)
# dataDictScenar = {'scenar_firstname':pd.Series(liste_scenas_firstname), 'scenar_lastname':pd.Series(liste_scenas_lastname)}
# dfCheckScenar = pd.DataFrame(dataDictScenar)

# df_people = pd.read_csv("csvImportData/csvPeople.csv", sep=";")

# Pour comparer les noms existants : https://stackoverflow.com/questions/20225110/comparing-two-dataframes-and-getting-the-differences
# Pour l'instant, pas d'attribution de char_id pour les people, à vérifier
# Pour cette màj, voir à cumuler une requête sur la base + suivre avec le check d'existence 

# for i in range(len(df_people)):
#     nom = df_people.loc[i, 'people_firstname']+ " " + df_people.loc[i,'people_lastname']
#     if nom in liste_reals:
#         df_people.loc[i,'is_rea'] = True
#     if nom in liste_scena:
#         df_people.loc[i,'is_scenar'] = True