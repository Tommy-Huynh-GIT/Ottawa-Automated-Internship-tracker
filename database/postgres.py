import psycopg2
from dotenv import load_dotenv
import os
from pathlib import Path
from notifications import notify_new_job

#load environment vars
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

#main will call this once to create the table
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
            company VARCHAR(255),
            application_status VARCHAR(50) DEFAULT 'not_started',
            application_notes TEXT,
            applied_at TIMESTAMP
        )
        """
    )
    cur.execute("ALTER TABLE job ADD COLUMN IF NOT EXISTS application_status VARCHAR(50) DEFAULT 'not_started'")
    cur.execute("ALTER TABLE job ADD COLUMN IF NOT EXISTS application_notes TEXT")
    cur.execute("ALTER TABLE job ADD COLUMN IF NOT EXISTS applied_at TIMESTAMP")
    #used to commit actions to database
    conn.commit()

    #close both
    cur.close()
    conn.close()


#Scrapers will call this so we can push to database
def save_job(link, title, company):
    conn = get_connection()
    cur = conn.cursor()

    #Insert the job into the database, use(%s, %s, %s) to avoid SQL injection
    cur.execute(
        """
        INSERT INTO job (link, title, company)
        VALUES (%s, %s, %s) 
        ON CONFLICT (link) DO NOTHING
        RETURNING id, link, title, company, application_status
        """,
        (link, title, company)
    )

    row = cur.fetchone()
    inserted_job = row is not None

    if row is None:
        cur.execute(
            """
            SELECT id, link, title, company, application_status
            FROM job
            WHERE link = %s
            """,
            (link,)
        )
        row = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()

    if inserted_job:
        notify_new_job(link, title, company)

    return {
        "id": row[0],
        "link": row[1],
        "title": row[2],
        "company": row[3],
        "application_status": row[4],
    }


def update_application_status(job_id, status, notes=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE job
        SET application_status = %s,
            application_notes = %s,
            applied_at = CASE WHEN %s = 'submitted' THEN NOW() ELSE applied_at END
        WHERE id = %s
        """,
        (status, notes, status, job_id)
    )

    conn.commit()

    cur.close()
    conn.close()
