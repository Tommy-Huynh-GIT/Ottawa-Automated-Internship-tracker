import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright

from main import SCRAPERS
from scrapers.links import is_trusted_job_url
from sites import sites


async def run_browser_smoke(headless):
    failures = []

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=headless, slow_mo=150)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})

        for site in sites:
            company = site["company"]
            print(f"\nBROWSER TEST -> {company}: {site['url']}", flush=True)

            try:
                if not is_trusted_job_url(site["url"], site["url"]):
                    raise ValueError("source URL is not a trusted HTTPS URL")

                await page.goto(site["url"], wait_until="domcontentloaded", timeout=60000)
                if not is_trusted_job_url(page.url, site["url"]):
                    raise ValueError(f"redirected to an untrusted host: {page.url}")

                try:
                    await page.wait_for_load_state("networkidle", timeout=10000)
                except PlaywrightTimeoutError:
                    pass

                jobs = await SCRAPERS[site["platform"]](
                    page,
                    company,
                    site.get("location_keywords"),
                )
                print(f"PASS {company}: {len(jobs)} matching job links", flush=True)
            except Exception as error:
                failures.append(f"{company}: {type(error).__name__}: {error}")
                print(f"FAIL {company}: {type(error).__name__}: {error}", flush=True)

        await browser.close()

    passed = len(sites) - len(failures)
    print(f"\nBROWSER TEST COMPLETE: {passed}/{len(sites)} sources passed", flush=True)
    for failure in failures:
        print(f"FAILURE: {failure}", flush=True)

    return not failures


def main():
    parser = argparse.ArgumentParser(description="Smoke-test every configured career source.")
    parser.add_argument(
        "--headed",
        action="store_true",
        help="show the Chromium browser while testing",
    )
    arguments = parser.parse_args()
    passed = asyncio.run(run_browser_smoke(headless=not arguments.headed))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()