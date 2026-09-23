from constants import KEYWORDS


async def icims(page, company):
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
            link = await job.get_attribute("href")

            if title and link:
                if KEYWORDS.search(title):
                    jobs.append({
                        "title": title,
                        "link": link,
                        "company": company,
                    })

    return jobs
