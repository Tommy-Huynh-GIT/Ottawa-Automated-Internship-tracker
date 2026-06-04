# Ottawa Internship Tracker

I built this project after finding that internship postings in Ottawa were scattered across different company career pages and hard to track in one place.

This app scrapes internship postings from selected company career sites, stores them in a PostgreSQL database, exposes the data through a read-only FastAPI backend, and displays the results in a simple React frontend.

## Features

- Scrapes internship and student job postings from company career pages
- Stores job title, company, and job link in PostgreSQL
- Avoids duplicate job entries by using each job link as a unique value
- Sends optional phone notifications when a brand new job is found
- Provides read-only API routes for jobs and companies
- Displays jobs in a React frontend with a company dropdown filter

## Tech Stack

- Python
- Selenium
- PostgreSQL
- FastAPI
- React
- Vite

## Project Structure

```text
SeleniumStuff/
  backend/
    main.py

  database/
    postgres.py

  frontend/
    src/
      App.jsx
      main.jsx
      styles.css

  scrapers/
    general.py
    icims.py
    oracle.py

  main.py
  sites.py
  constants.py
```

## How It Works

```text
Selenium scraper
  -> finds internship postings
  -> saves jobs into PostgreSQL
  -> sends a phone notification for newly inserted jobs

FastAPI backend
  -> reads jobs from PostgreSQL
  -> returns JSON

React frontend
  -> calls the backend
  -> displays jobs by company
```

## API Routes

```text
GET /jobs
```

Returns all jobs.

```text
GET /jobs?company=Nokia
```

Returns jobs for a specific company.

```text
GET /companies
```

Returns all unique company names for the dropdown menu.

## Environment Variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_PORT=5432
NTFY_TOPIC=ottawainternships_alert
```

## Phone Notifications

Phone notifications are handled through [ntfy](https://ntfy.sh/). This is
optional; if `NTFY_TOPIC` is missing from `.env`, the scraper still saves jobs
but does not send phone alerts.

To enable alerts:

1. Install the ntfy app on your phone.
2. Subscribe to the same topic name you put in `.env`.
3. Run the scraper normally.

When the scraper finds a matching job, PostgreSQL tries to insert the job link.
If the link is new, the insert succeeds and a phone notification is sent. If the
link already exists in the database, PostgreSQL ignores it and no duplicate
notification is sent.

The example topic is:

```env
NTFY_TOPIC=ottawainternships_alert
```

For privacy, use a harder-to-guess topic name before relying on this long term.
Anyone who knows the topic name can subscribe to it.

## Running The Project

Run the scraper from the project root:

```powershell
python main.py
```

Or use the batch runner, which also writes output to `logs/scraper.log`:

```powershell
.\run_scraper.bat
```

Start the backend from the project root:

```powershell
python -m uvicorn backend.main:app --reload
```

Start the frontend in a second terminal:

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

Then open:

```text
http://localhost:5173
```

## Notes

The frontend is read-only. Users can view and filter jobs, but they cannot create, edit, or delete database records. The scraper is responsible for writing new jobs into the database.
