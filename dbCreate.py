# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 14:21:17 2021

@author: Ga
"""

# import the PostgreSQL client for Python

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT #permet de créer la DB
from psycopg2 import Error

try:
    conn = psycopg2.connect(user="postgres",
                              password="8774755Garapostgresql!",
                              host="127.0.0.1",
                              port="5432",
                              database="postgres")
    
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
    
    # Obtain a DB Cursor
    cursor = conn.cursor()
    
    cursor.execute("""CREATE DATABASE kaam_db
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;""")

except (Exception, Error) as error:
    print("Unable to connect to the database", error)
    
finally:
    if conn:
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")
