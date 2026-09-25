import asyncio
import os

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

from application_automation import ApplicationAutomator, load_applicant_profile
from database.postgres import create_tables, save_job, update_application_status
from scrapers.general import general_scraper
from scrapers.icims import icims
from scrapers.links import is_trusted_job_url
from scrapers.oracle import oracle
from sites import sites


SCRAPERS = {
    "Custom": general_scraper,
    "Workday": general_scraper,
    "ICIMS": icims,
    "Oracle": oracle,
}


def env_flag(name, default=False):
    value = os.getenv(name)

    if value is None:
        return default

    return value.lower() in ["1", "true", "yes", "on"]


async def scrape_site(page, site):
    company = site["company"]
    platform = site["platform"]
    url = site["url"]
    scraper = SCRAPERS.get(platform, general_scraper)

    if not is_trusted_job_url(url, url):
        print(f"Skipped {company}: source URL is not a trusted HTTPS URL")
        return []

    await page.goto(url, wait_until="domcontentloaded", timeout=60000)

    try:
        await page.wait_for_load_state("networkidle", timeout=10000)
    except PlaywrightTimeoutError:
        pass

    if not is_trusted_job_url(page.url, url):
        print(f"Skipped {company}: redirected to an untrusted host ({page.url})")
        return []

    return await scraper(page, company, site.get("location_keywords"))


async def main():
    create_tables()

    auto_apply = env_flag("AUTO_APPLY", False)
    auto_submit = env_flag("AUTO_SUBMIT_APPLICATIONS", False)
    headless = env_flag("HEADLESS", True)
    saved_jobs = []

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=headless)
        context = await browser.new_context()
        page = await context.new_page()

        for site in sites:
            try:
                scraped_jobs = await scrape_site(page, site)
            except PlaywrightTimeoutError as error:
                print(f"Skipped {site['company']} after timeout: {error}")
                continue

            for job in scraped_jobs:
                saved_job = save_job(job["link"], job["title"], job["company"])
                saved_jobs.append(saved_job)

        if auto_apply:
            profile = load_applicant_profile()
            automator = ApplicationAutomator(profile, submit=auto_submit)

            for job in saved_jobs:
                if job["application_status"] in ["submitted", "ready_to_submit"]:
                    continue

                application_page = await context.new_page()
                result = await automator.apply_to_job(application_page, job)
                update_application_status(job["id"], result.status, result.notes)
                await application_page.close()

                print(f"{job['company']} - {job['title']}: {result.status}")
                print(result.notes)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
