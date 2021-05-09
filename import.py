# -*- coding: utf-8 -*-
"""
Created on Sat May  8 12:15:44 2021

@author: Ga
"""

from sqlalchemy.exc import SQLAlchemyError
import yaml
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import types
from sqlalchemy.dialects import postgresql
import sqlalchemy

dir = r'C:\Users\Ga\Documents\GitHub\Kaam_proj'
os.chdir(dir)

login = yaml.safe_load(open('logins.yml', 'r'))
login = login['postgres']

colNames = ["ep_id","livre","num_ep","titre_ep","script","resume_vf","resume_va"]
dfEpisodes = pd.read_csv('csvEpisode.csv', sep=';', names=colNames)
user=login['user']
password=login['password']
host="localhost"
port="5432"
database="kaam_db"

test = sqlalchemy.dialects.postgresql.smallint


dataTypes={'ep_id': sqlalchemy.dialects.postegresql.smallserial,
           'livre': sqlalchemy.dialects.postegresql.smallint,
           'num_ep': sqlalchemy.dialects.postegresql.smallint,
           'titre_ep': sqlalchemy.dialects.postegresql.varchar(100),
           'script': sqlalchemy.dialects.postegresql.varchar(10000),
           'resume_vf': sqlalchemy.dialects.postegresql.varchar(1000),
           'resume_va': sqlalchemy.dialects.postegresql.varchar(1000)}

# In[0] : Création des tables de la bdd kaam_db

try:    
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    dbConnection = engine.connect()
    dfEpisodes.to_sql('episode2', engine, if_exists='replace', dtype=dataTypes)
    print("Table 'episode' successfully updated in PostgreSQL")
    
    
except (Exception, SQLAlchemyError()) as error:
    print("Unable to connect to the database", error)
        
finally:
    dbConnection.close()
    print("PostgreSQL connection is closed")