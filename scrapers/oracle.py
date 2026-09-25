from constants import KEYWORDS
from scrapers.links import normalize_job_link


async def oracle(page, company, location_keywords=None):
    print(f"NOW SCRAPING {company}!")
    print("====================================")

    jobs = []

    if company in ["Nokia", "Ross Video"]:
        job_links = page.locator("a.job-grid-item__link")

        await job_links.first.wait_for(timeout=20000)

        count = await job_links.count()

        for index in range(count):
            job = job_links.nth(index)

            # This gives us an id for the element that holds the job title.
            labelled_by = await job.get_attribute("aria-labelledby")
            title = ""

            if labelled_by:
                title_element = page.locator(f"[id='{labelled_by}']")
                title = (await title_element.inner_text()).strip()

            link = normalize_job_link(await job.get_attribute("href"), page.url)

            if title and link:
                if KEYWORDS.search(title):
                    jobs.append({
                        "title": title,
                        "link": link,
                        "company": company,
                    })

    return jobs
