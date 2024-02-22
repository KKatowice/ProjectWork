""" connection = mysql.connector.connect(
    host="team2-proj-project-work.a.aivencloud.com",
    user="avnadmin",
    password="AVNS_R6OpJnjvrGcYTzCaBPv",
    database="defaultdb",
    port=19066,
    charset="utf8mb4",
    connect_timeout=timeout,
) """



import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()
id = os.getenv('ID') #avnadmin
psw = os.getenv('PSW')#AVNS_R6OpJnjvrGcYTzCaBPv
h = os.getenv('H') #team2-proj-project-work.a.aivencloud.com
p = os.getenv('PRT') #19066
DBNAME = 'concessionario'

def create_server_connection():
    connection = None
    try:
        print(h,id,psw)
        connection = mysql.connector.connect(
            host=h,
            user=id,
            password=psw,
            #database=DBNAME,
            port=p,
            charset="utf8mb4",
            connect_timeout=120,auth_plugin='caching_sha2_password'
        ) 
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def create_db_connection(dbn = DBNAME):
    print("sissi arrivo qui")
    connection = None
    try:
        connection = mysql.connector.connect(
            host=h,
            user=id,
            password=psw,
            database=dbn,
            port=p,
            charset="utf8mb4",
            connect_timeout=10,
        ) 
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


def execute_query(connection, query, mu=False): #
    cursor = connection.cursor()
    try:
        if mu:
            if len(query) == 0: return
            for x in query:
                cursor.execute(x)
        else:
            print(query)
            cursor.execute(query)#,multi=mu
        connection.commit()
    except Error as err:
        print(f"Failed query: '{query}'")
        print(f"Error: '{err}'")
    finally:
        cursor.close()

def execute_query2(connection, query, mu=False): #
    cursor = connection.cursor()
    try:
        if mu:
            if len(query) == 0: return
            for x in query:
                cursor.execute(x)
        else:
            print(query)
            cursor.execute(query)#,multi=mu

    except Error as err:
        print(f"Failed query: '{query}'")
        print(f"Error: '{err}'")
    finally:
        cursor.close()

def read_query(connection, query:str, dic = True):
    cursor = connection.cursor(dictionary=dic)
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Failed query: '{query}'")
        print(f"Error: '{err}'")
        
    finally:
        cursor.close()

def execute_many_query(connection, query, lista):
    cursor = connection.cursor()
    try:
        cursor.executemany(query, lista)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")