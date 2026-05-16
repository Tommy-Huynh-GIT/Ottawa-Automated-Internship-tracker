import { useEffect, useState } from "react";

const API_URL = "http://localhost:8000";

function App() {
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState("All");
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadCompanies() {
      try {
        const response = await fetch(`${API_URL}/companies`);

        if (!response.ok) {
          throw new Error("Could not load companies");
        }

        const data = await response.json();
        setCompanies(data);
      } catch (err) {
        setError(err.message);
      }
    }

    loadCompanies();
  }, []);

  useEffect(() => {
    async function loadJobs() {
      setLoading(true);
      setError("");

      try {
        const url =
        //If Selectedcompany === All then grab all jobs else grab specified company
          selectedCompany === "All"
            ? `${API_URL}/jobs`
            : `${API_URL}/jobs?company=${encodeURIComponent(selectedCompany)}`;

        const response = await fetch(url);

        if (!response.ok) {
          throw new Error("Could not load jobs");
        }

        const data = await response.json();
        setJobs(data);
      } catch (err) {
        setError(err.message);
        setJobs([]);
      } finally {
        setLoading(false);
      }
    }

    loadJobs();
  }, [selectedCompany]);

  return (
    <main className="page">
      <section className="sidebar">
        <h1>Job Tracker</h1>

        <label htmlFor="company">Company</label>
        <select
          id="company"
          value={selectedCompany}
          onChange={(event) => setSelectedCompany(event.target.value)}
        >
          <option value="All">All</option>
          {companies.map((company) => (
            <option key={company} value={company}>
              {company}
            </option>
          ))}
        </select>
      </section>

      <section className="content">
        <div className="contentHeader">
          <h2>{selectedCompany === "All" ? "All Jobs" : selectedCompany}</h2>
          <p>{jobs.length} jobs</p>
        </div>

        {error && <p className="message error">{error}</p>}
        {loading && <p className="message">Loading jobs...</p>}

        {!loading && !error && jobs.length === 0 && (
          <p className="message">No jobs found.</p>
        )}

        <div className="jobs">
          {jobs.map((job) => (
            <article className="job" key={job.id}>
              <h3>{job.title}</h3>
              <p>{job.company}</p>
              <a href={job.link} target="_blank" rel="noreferrer">
                Open job
              </a>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

export default App;
