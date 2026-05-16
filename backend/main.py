from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database.postgres import get_connection 


app = FastAPI()

@app.get("/")
def root():
    return {"Hello" : "World"}


#Returns the jobs for the specific 
@app.get("/jobs")
#Could take a query parameter company or none at all (for the all case)
def get_jobs(company: str | None = None):
    #create the connection to database
    conn = get_connection()
    #used to execute commands
    cur = conn.cursor()

    if company:
        #select specific company
        cur.execute("""SELECT * FROM job WHERE company = %s,
        (company,)
""")
    else:
        #select all jobs
        cur.execute("""SELECT * from job""")

    #collect all the jobs
    rows = cur.fetchall()

    cur.close()
    conn.close()

    jobs = []

    for row in rows:
        #used object here because returning job with multiple details
        jobs.append({
            "id": row[0], #first index in the tuple is id and vice versa
            "link" : row[1],
            "title": row[2],
            "company": row[3]
        })

    return jobs
        
        


#this will get all companies for the dropdown menu 
@app.get("/companies")
def get_company():
    #create the connection to database
    conn = get_connection()
    #used to execute commands
    cur = conn.cursor()

    #select all companies
    cur.execute("""SELECT DISTINCT company FROM job ORDER BY company
""")
    
    rows = cur.fetchall()

    companies = []

    for row in rows:
        #used list instead of an object because just returning many things with no details
        companies.append(row[0])
    return companies

