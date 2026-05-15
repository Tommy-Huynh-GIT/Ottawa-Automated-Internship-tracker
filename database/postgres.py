import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()

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

cur.execute("""CREATE TABLE IF NOT EXISTS job (
            id SERIAL PRIMARY KEY,
            link TEXT UNIQUE,
            title TEXT,
            company VARCHAR(255)
            )

        """)


#used to commit actions to database
conn.commit()

#close cursor and database
cur.close()
conn.close()
