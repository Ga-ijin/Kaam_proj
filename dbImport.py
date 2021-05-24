# -*- coding: utf-8 -*-
"""
Created on Tue May 11 11:14:27 2021

@author: Ga
"""

import yaml
import os
import pandas as pd
from sqlalchemy import create_engine, types

dir = r'C:\Users\Ga\Documents\GitHub\Kaam_proj'
os.chdir(dir)

login = yaml.safe_load(open('logins.yml', 'r'))
login = login['postgres']
user=login['user']
password=login['password']
host="localhost"
port="5432"
database="kaam_db2"

def maxLen(dfColumn):
    maxLen = pd.DataFrame()
    maxLen["max length"] = dfColumn.str.len()
    maxLen = maxLen['max length'].max()
    return(maxLen)

# Création des tables de la bdd kaam_db

try:    
    episode = pd.read_csv('csvImportData/csvEpisode2.csv', sep=";")
    lenTitreEp =maxLen(episode['titre_ep'])
    lenScript =maxLen(episode['script'])
    lenResumeVF =maxLen(episode['resume_vf'])
    lenResumeVA =maxLen(episode['resume_va'])
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    dbConnection = engine.connect()

# In[1] : Table épisode
    episode.to_sql('episode',
                    engine,
                    if_exists='replace',
                    index = False,
                    dtype=
                        {'ep_id': types.SmallInteger,
                        'livre': types.SmallInteger,
                        'num_ep': types.SmallInteger,
                        'titre_ep': types.VARCHAR(lenTitreEp),
                        'script': types.VARCHAR(lenScript),
                        'resume_vf': types.VARCHAR(lenResumeVF),
                        'resume_va': types.VARCHAR(lenResumeVA)
                        }
                    )
    print("Table 'episode' created successfully in PostgreSQL")
    
# In[2] : Table rating
    rating = pd.read_csv('csvImportData/csvRating.csv', sep=";")
    rating.to_sql('rating',
                    engine,
                    if_exists='replace',
                    index = False,
                    dtype=
                        {'ep_id': types.SmallInteger,
                         'rating': types.FLOAT,
                         'nb_votes': types.SmallInteger}
                    )
    print("Table 'rating' created successfully in PostgreSQL")
    
# In[3] : Table casting
    casting = pd.read_csv('csvImportData/csvCasting.csv', sep=";")
    casting.to_sql('casting',
                    engine,
                    if_exists='replace',
                    index = False,
                    dtype=
                        {'ep_id': types.SmallInteger,
                         'char_id': types.SmallInteger}
                    )
    print("Table 'casting' created successfully in PostgreSQL")

# In[4] : Table character
    charac = pd.read_csv('csvImportData/csvCharacters.csv', sep=";")
    lenCharName =maxLen(charac['char_name'])
    lenCharDescr =maxLen(charac['char_descr'])
    
    charac.to_sql('character',
                    engine,
                    if_exists='replace',
                    index = False,
                    dtype=
                        {'char_id': types.SmallInteger,
                         'char_name': types.VARCHAR(lenCharName),
                         'char_descr': types.VARCHAR(lenCharDescr),
                         'knight': types.BOOLEAN
                         }
                    )
    print("Table 'character' created successfully in PostgreSQL")
    
# In[5] : Table character
    people = pd.read_csv('csvImportData/csvPeople.csv', sep=";")
    lenFirstName =maxLen(people['people_firstname'])
    lenLastName =maxLen(people['people_lastname'])
    
    people.to_sql('people',
                    engine,
                    if_exists='replace',
                    index = False,
                    dtype=
                        {'people_id': types.SmallInteger,
                         'char_id': types.SmallInteger,
                         'people_firstname': types.VARCHAR(lenFirstName),
                         'people_lastname': types.VARCHAR(lenLastName)}
                        )
    print("Table 'people' created successfully in PostgreSQL")
    
# In[6] : Table crew
    crew = pd.read_csv('csvImportData/csvCrew.csv', sep=";")
    crew.to_sql('crew',
                    engine,
                    if_exists='replace',
                    index = False,
                    dtype=
                        {'ep_id': types.SmallInteger,
                         'people_id': types.SmallInteger}
                    )
    print("Table 'crew' created successfully in PostgreSQL")
        
finally:
    dbConnection.close()
    print("PostgreSQL connection is closed")