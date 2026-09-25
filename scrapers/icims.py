from constants import KEYWORDS
from scrapers.links import is_trusted_job_url, normalize_job_link
from urllib.parse import urljoin


async def icims(page, company, location_keywords=None):
    print(f"NOW SCRAPING {company}!")
    print("====================================")

    jobs = []

    if company == "Kinaxis":
        frame = page.frame_locator("#icims_content_iframe")
        job_links = frame.locator("a[href*='/jobs/'][href*='/job']")

        await job_links.first.wait_for(timeout=20000)

        count = await job_links.count()

        print("Kinaxis jobs found:", count)

        for index in range(count):
            job = job_links.nth(index)
            title = (await job.inner_text()).replace("Title", "").strip()
            iframe_source = await page.locator("#icims_content_iframe").get_attribute("src")
            frame_url = urljoin(page.url, iframe_source) if iframe_source else page.url
            if not is_trusted_job_url(frame_url, page.url):
                frame_url = page.url
            link = normalize_job_link(await job.get_attribute("href"), frame_url)

            if title and link:
                if KEYWORDS.search(title):
                    jobs.append({
                        "title": title,
                        "link": link,
                        "company": company,
                    })

    return jobs
