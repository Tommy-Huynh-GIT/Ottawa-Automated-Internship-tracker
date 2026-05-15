import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()

#Scrappers will call this so we can push to database 
def save_job(link, title, company):
    conn = psycopg2.connect(...)
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


#import values from .env file
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

#create connection object
conn = psycopg2.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT
)

#used to execute commands
cur = conn.cursor()

#create the table
cur.execute("""CREATE TABLE IF NOT EXISTS job (
            id SERIAL PRIMARY KEY,
            link TEXT UNIQUE,
            title TEXT,
            company VARCHAR(255)
            )
        """)

#
cur.execute("""INSERT INTO job (link, title, company)
            VALUES
            
        """)


#used to commit actions to database
conn.commit()

#close cursor and database
cur.close()
conn.close()
