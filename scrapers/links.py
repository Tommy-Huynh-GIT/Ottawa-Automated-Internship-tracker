from urllib.parse import urljoin, urlparse

TRUSTED_ATS_HOSTS = {
    "bamboohr.com",
    "careers.smartrecruiters.com",
    "greenhouse.io",
    "icims.com",
    "jobvite.com",
    "jobs.ashbyhq.com",
    "jobs.lever.co",
    "myworkdayjobs.com",
    "oraclecloud.com",
    "successfactors.com",
    "ultipro.ca",
    "workable.com",
}


def normalize_job_link(link, source_url):
    if not link:
        return None

    stripped_link = link.strip()
    if not stripped_link or stripped_link.startswith(("#", "//")):
        return None

    normalized_link = urljoin(source_url, stripped_link)
    if not is_trusted_job_url(normalized_link, source_url):
        return None

    return normalized_link


def is_trusted_job_url(candidate_url, source_url, allow_trusted_ats=True):
    source = urlparse(source_url)
    candidate = urlparse(candidate_url)

    if (
        candidate.scheme != "https"
        or not candidate.netloc
        or candidate.username
        or candidate.password
    ):
        return False

    if candidate.hostname == source.hostname:
        return True

    if not allow_trusted_ats:
        return False

    return any(
        candidate.hostname == trusted_host
        or candidate.hostname.endswith(f".{trusted_host}")
        for trusted_host in TRUSTED_ATS_HOSTS
    )


def is_likely_job_link(link):
    path = urlparse(link).path.casefold()
    query = urlparse(link).query.casefold()
    job_markers = (
        "/job",
        "/career/",
        "/careers/",
        "/position",
        "/opportunit",
        "/requisition",
        "/posting",
        "/apply",
    )

    return (
        any(marker in path for marker in job_markers)
        or "jobid=" in query
        or urlparse(link).hostname in TRUSTED_ATS_HOSTS
    )