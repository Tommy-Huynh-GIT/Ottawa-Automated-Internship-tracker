# Ottawa Internship Tracker

I built this project after finding that internship postings in Ottawa were scattered across different company career pages and hard to track in one place.

This app scrapes internship postings from selected company career sites with Playwright, stores them in a PostgreSQL database, exposes the data through a read-only FastAPI backend, and displays the results in a simple React frontend. It can also open saved postings and draft application forms from a local applicant profile.

## Features

- Scrapes internship and student job postings from company career pages with Playwright
- Stores job title, company, and job link in PostgreSQL
- Avoids duplicate job entries by using each job link as a unique value
- Sends optional phone notifications when a brand new job is found
- Tracks application status and notes for each saved job
- Optionally opens job applications, fills common profile fields, uploads a resume, and stops before final submit by default
- Provides read-only API routes for jobs and companies
- Displays jobs in a React frontend with a company dropdown filter

## Tech Stack

- Python
- Playwright
- PostgreSQL
- FastAPI
- React
- Vite

## Project Structure

```text
Ottawa-Automated-Internship-tracker/
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
    links.py
    oracle.py

  application_automation.py
  applicant_profile.example.json
  main.py
  sites.py
  constants.py
```

## Sources

The tracker covers Ottawa and Kanata technology, telecom, aerospace, defence,
software, and research employers. Sources include Nokia, Kinaxis, Ciena, Cisco,
Ericsson, Solace, MDA Space, Telesat, Calian, ADGA, Thales, Lockheed Martin,
BlackBerry/QNX, Ross Video, March Networks, Ranovus, thinkRF, Wind River,
Ribbon Communications, Skyworks, Semtech, Microchip, Synopsys, Keysight,
Amdocs, Pythian, L3Harris, Kongsberg Geospatial, TrendAI, NRC, CSE, and other
Ottawa-area employers.

Where available, sources point directly to internship, co-op, student, or job
search pages. For example, MDA Space uses its co-op/student board and Thales
uses its Students and Graduates page. Some companies currently expose only a
general careers page and may return zero matching postings until an internship
is published.

## How It Works

```text
Playwright scraper
  -> finds internship postings
  -> saves jobs into PostgreSQL
  -> sends a phone notification for newly inserted jobs

Playwright application automator
  -> opens saved postings
  -> clicks apply where available
  -> fills common profile fields
  -> uploads resume when configured
  -> records application status

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

Install Python dependencies:

```powershell
pip install -r requirements.txt
python -m playwright install chromium
```

Run the scraper from the project root:

```powershell
python main.py
```

Run the Python tests:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Run the TrendAI browser smoke test in a visible Chromium window:

```powershell
npx playwright test tests/trendai.spec.ts --project=chromium --headed
```

The full browser smoke run opens every configured source and exercises its
assigned scraper. It is a read-only diagnostic and does not write jobs to
PostgreSQL:

```powershell
python tests/browser_smoke.py --headed
```

Optional automation controls:

```env
AUTO_APPLY=false
AUTO_SUBMIT_APPLICATIONS=false
HEADLESS=true
APPLICANT_PROFILE_PATH=applicant_profile.json
```

`AUTO_SUBMIT_APPLICATIONS` is intentionally separate from `AUTO_APPLY`. Draft mode is the default because every employer form is a little different, and final submission should be reviewed before it is sent.

Or use the batch runner, which also writes output to `logs/scraper.log`:

```powershell
.\run_scraper.bat
```

To draft applications, create a private profile:

```powershell
Copy-Item applicant_profile.example.json applicant_profile.json
```

Fill in `applicant_profile.json`, then run:

```powershell
$env:AUTO_APPLY="true"
$env:HEADLESS="false"
python main.py
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

The frontend is read-only. Users can view and filter jobs, but they cannot create, edit, or delete database records. The scraper and application automator are responsible for writing new jobs and application statuses into the database.

Application automation is best-effort because each company uses a different career platform. The bot fills common labelled fields and file inputs, then records whether the application is ready to submit, submitted, failed, or needs manual review.
