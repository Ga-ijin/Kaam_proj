# -*- coding: utf-8 -*-
"""
Created on Wed May  5 09:52:41 2021

@author: Greta
"""

import psycopg2
from psycopg2 import Error
import yaml

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
    
    # create_fk_rating = ''' ALTER TABLE rating
    #                     ADD CONSTRAINT fk_rating_ep
    #                     FOREIGN KEY(ep_id)
    #                     REFERENCES episode(ep_id)
    #                     ON DELETE CASCADE
    #                     ON UPDATE CASCADE;'''
    # cursor.execute(create_fk_rating)
    # conn.commit()
    # print("FK 'fk_rating_ep' created successfully in PostgreSQL")
    
    # create_fks_casting_ep_char = ''' ALTER TABLE casting
    #                         ADD CONSTRAINT fk_casting_ep
    #                         FOREIGN KEY(ep_id)
    #                         REFERENCES episode(ep_id)
    #                         ON DELETE CASCADE
    #                         ON UPDATE CASCADE;
    #                         ALTER TABLE casting
    #                         ADD CONSTRAINT fk_casting_char
    #                         FOREIGN KEY(char_id)
    #                         REFERENCES character(char_id)
    #                         ON DELETE CASCADE
    #                         ON UPDATE CASCADE;'''
    # cursor.execute(create_fks_casting_ep_char)
    # conn.commit()
    # print("FK 'fk_casting_ep_char' created successfully in PostgreSQL")
    
    create_fk_people = ''' ALTER TABLE people
                            ADD CONSTRAINT fk_people_char
                            FOREIGN KEY(char_id)
                            REFERENCES character(char_id)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE;'''
    cursor.execute(create_fk_people)
    conn.commit()
    print("FK 'fk_people_char' created successfully in PostgreSQL")
    
    create_fks_crew_ep_people = ''' ALTER TABLE crew
                            ADD CONSTRAINT fk_crew_ep
                            FOREIGN KEY(ep_id)
                            REFERENCES episode(ep_id)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE;
                            ALTER TABLE crew
                            ADD CONSTRAINT fk_crew_people
                            FOREIGN KEY(people_id)
                            REFERENCES people(people_id)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE;'''
    cursor.execute(create_fks_crew_ep_people)
    conn.commit()
    print("FK 'fks_crew_ep_people' created successfully in PostgreSQL")

except (Exception, Error) as error:
    print("Unable to connect to the database", error)
    
finally:
    if conn:
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")
