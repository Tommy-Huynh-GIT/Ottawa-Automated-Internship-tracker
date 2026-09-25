from constants import KEYWORDS
from scrapers.links import is_likely_job_link, normalize_job_link


async def general_scraper(page, company, location_keywords=None):
    print(f"NOW SCRAPING {company}!")
    print("====================================")

    if company == "General Dynamics":
        # Anchor tags that hold the right links don't have classes.
        job_links = page.locator("a:not([class])")
    elif company == "Cisco":
        job_links = page.locator("a[href*='/global/en/job/']:visible")
    else:
        job_links = page.locator("a")

    if company == "Cisco":
        await job_links.first.wait_for(timeout=20000)

    jobs = []
    count = await job_links.count()

    for index in range(count):
        job = job_links.nth(index)
        title = (await job.inner_text()).strip()
        link = normalize_job_link(await job.get_attribute("href"), page.url)

        if title and link and is_likely_job_link(link):
            if location_keywords and not any(
                keyword.casefold() in title.casefold() for keyword in location_keywords
            ):
                continue

            if company == "Cisco" and "Canada" not in title:
                continue

            if KEYWORDS.search(title):
                jobs.append({
                    "title": title,
                    "link": link,
                    "company": company,
                })

    return jobs


# Backwards-compatible name while the rest of the project moves to snake_case.
generalScrapper = general_scraper
