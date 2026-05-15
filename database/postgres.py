import psycopg2
from dotenv import load_dotenv
import os
from pathlib import Path

#load environemnt vars
load_dotenv()


#import values from .env file
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

#connection function
def get_connection():
    #create connection object
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

#
def create_tables():
    conn = get_connection()
    #used to execute commands
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS job (
            id SERIAL PRIMARY KEY,
            link TEXT UNIQUE,
            title TEXT,
            company VARCHAR(255)
        )
        """
    )
    #used to commit actions to database
    conn.commit()

    #close both
    cur.close()
    conn.close()


#Scrappers will call this so we can push to database 
def save_job(link, title, company):
    conn = get_connection()
    cur = conn.cursor()

    #Insert the job into the database, use(%s, %s, %s) to avoid SQL injection
    cur.execute(
        """
        INSERT INTO job (link, title, company)
        VALUES (%s, %s, %s) 
        ON CONFLICT (link) DO NOTHING
        """,
        (link, title, company)
    )

    conn.commit()

    cur.close()
    conn.close()
