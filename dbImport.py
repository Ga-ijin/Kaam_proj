# -*- coding: utf-8 -*-
"""
Created on Tue May 11 11:14:27 2021

@author: Ga
"""

from sqlalchemy.exc import SQLAlchemyError
import yaml
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import types

dir = r'C:\Users\Ga\Documents\GitHub\Kaam_proj'
os.chdir(dir)

login = yaml.safe_load(open('logins.yml', 'r'))
login = login['postgres']
user=login['user']
password=login['password']
host="localhost"
port="5432"
database="kaam_db"

# Création des tables de la bdd kaam_db

try:    
    content = pd.read_csv('csvImportData/csvEpisode.csv', sep=";")
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    dbConnection = engine.connect()
    
    content.to_sql('episode2',
                    engine,
                    if_exists='replace',
                    dtype=
                        {'ep_id': types.SmallInteger,
                        'livre': types.SmallInteger,
                        'num_ep': types.SmallInteger,
                        'titre_ep': types.VARCHAR,
                        'script': types.VARCHAR,
                        'resume_vf': types.VARCHAR,
                        'resume_va': types.VARCHAR
                        }
                    )
    
except (Exception, SQLAlchemyError()) as error:
    print("Unable to connect to the database", error)
        
finally:
    dbConnection.close()
    print("PostgreSQL connection is closed")