# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 18:01:26 2021

@author: Ga
"""
import psycopg2
from psycopg2 import Error
import yaml
import os

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
    
    create_table_ep ='''CREATE TABLE episode
                            (ep_id SMALLSERIAL PRIMARY KEY,
                            livre SMALLINT NOT NULL,
                            num_ep SMALLINT NOT NULL,
                            titre_ep VARCHAR (100) NOT NULL,
                            script VARCHAR (10000) NOT NULL,
                            resume_vf VARCHAR (1000),
                            resume_va VARCHAR (1000)); '''
         
    cursor.execute(create_table_ep)
    conn.commit()
    print("Table 'episode' created successfully in PostgreSQL")
    
    create_table_rating ='''CREATE TABLE rating
                                (ep_id SMALLSERIAL NOT NULL,
                                rating DECIMAL,
                                nb_votes SMALLINT); '''
    
    cursor.execute(create_table_rating)
    conn.commit()
    print("Table 'rating' created successfully in PostgreSQL")
     
    create_table_casting ='''CREATE TABLE casting
                                (ep_id SMALLSERIAL NOT NULL,
                                char_id SMALLSERIAL NOT NULL); '''
         
    cursor.execute(create_table_casting)
    conn.commit()
    print("Table 'casting' created successfully in PostgreSQL")
  
    create_table_character ='''CREATE TABLE character 
                                    (char_id SMALLSERIAL PRIMARY KEY,
                                    char_name VARCHAR (100) NOT NULL,
                                    char_descr VARCHAR (1000),
                                    knight BOOLEAN NOT NULL); '''
         
    cursor.execute(create_table_character)
    conn.commit()
    print("Table 'character' created successfully in PostgreSQL")
    
    create_table_people ='''CREATE TABLE people
                                (people_id SMALLSERIAL PRIMARY KEY,
                                char_id SMALLSERIAL NOT NULL,
                                people_firstname VARCHAR (50) NOT NULL,
                                people_lastname VARCHAR (50)); '''
 
    cursor.execute(create_table_people)
    conn.commit()
    print("Table 'people' created successfully in PostgreSQL")
    
    create_table_crew ='''CREATE TABLE crew
                            (ep_id SMALLSERIAL NOT NULL,
                            people_id SMALLINT NOT NULL,
                            is_rea BOOLEAN NOT NULL,
                            is_scenar BOOLEAN NOT NULL); '''
                             
    cursor.execute(create_table_crew)
    conn.commit()
    print("Table 'crew' created successfully in PostgreSQL")

except (Exception, Error) as error:
    print("Unable to connect to the database", error)
    
finally:
    if conn:
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")
        
        
# # Example
# def run_method(n):
#     for i in range(n):
#         3 ** nfrom timeit import default_timer as timer
# start_time = timer()
# run_method(10000)
# end_time = timer()
# elapsed = end_time-start_time
# print('function took {:.3f} ms'.format((elapsed)*1000.0))