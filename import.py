# -*- coding: utf-8 -*-
"""
Created on Sat May  8 12:15:44 2021

@author: Ga
"""
import psycopg2
from psycopg2 import Error
import yaml
import os
# import pandas as pd

dir = r'C:\Users\Ga\Documents\GitHub\Kaam_proj'
os.chdir(dir)

login = yaml.safe_load(open('logins.yml', 'r'))
login = login['postgres']

# Création des tables de la bdd kaam_db



try:    
    conn = psycopg2.connect(user=login['user'],
                              password=login['password'],
                              host="127.0.0.1",
                              port="5432",
                              database="kaam_db")    
    cursor = conn.cursor()
    
    # csv = open('csvEpisode.csv')
    # cursor.copy_from(csv, 'episode', sep=";")
    
    with open('csvEpisode.csv') as f:
        # next(f)
        cursor.copy_from(f, "episode", columns=("ep_id","livre","num_ep","titre_ep","script",'resume_vf',"resume_va"), sep=";")


    conn.commit()
    print("Table 'episode' successfully updated in PostgreSQL")
    
    
except (Exception, Error) as error:
    print("Unable to connect to the database", error)
        
finally:
    if conn:
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")

    # with open('csvFinal.csv', 'r') as data:
    #     next(data) # Skip the header row.
    #     cursor.copy_from(data, 'episode', sep=';')
        # cur.copy_from(csv, 'episode', columns=('col1', 'col2'), sep=",")
# con.commit()
    
#     upload_table_episode ='''COPY episode
#         FROM 'csvEpisode.csv'
#         DELIMITER ';' CSV;
#         '''
    # cursor.execute(upload_table_episode)