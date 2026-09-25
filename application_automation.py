import json
import os
from dataclasses import dataclass
from pathlib import Path
from re import Pattern

from playwright.async_api import Error as PlaywrightError
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError
from scrapers.links import is_trusted_job_url
from sites import sites


APPLY_TEXT = r"apply|apply now|start application|submit application"


@dataclass
class ApplicationResult:
    status: str
    notes: str


def load_applicant_profile(path=None):
    profile_path = Path(path or os.getenv("APPLICANT_PROFILE_PATH", "applicant_profile.json"))

    if not profile_path.exists():
        raise FileNotFoundError(
            f"Applicant profile not found at {profile_path}. "
            "Copy applicant_profile.example.json to applicant_profile.json and fill it in."
        )

    with profile_path.open("r", encoding="utf-8") as profile_file:
        return json.load(profile_file)


class ApplicationAutomator:
    def __init__(self, profile, submit=False, screenshot_dir="artifacts/applications"):
        self.profile = profile
        self.submit = submit
        self.screenshot_dir = Path(screenshot_dir)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    async def apply_to_job(self, page: Page, job):
        try:
            if not self._is_trusted_job(job):
                return ApplicationResult(
                    "failed",
                    "Stopped before navigation because the stored job URL is untrusted.",
                )

            await page.goto(job["link"], wait_until="domcontentloaded", timeout=60000)
            if not is_trusted_job_url(page.url, job["link"], allow_trusted_ats=False):
                return ApplicationResult(
                    "failed",
                    "Stopped before form interaction because the job page redirected to an untrusted host.",
                )

            await self._settle(page)
            page = await self._open_apply_flow(page)
            if not is_trusted_job_url(page.url, job["link"], allow_trusted_ats=False):
                return ApplicationResult(
                    "failed",
                    "Stopped before form interaction because the application page is untrusted.",
                )

            await self._settle(page)
            if not is_trusted_job_url(page.url, job["link"], allow_trusted_ats=False):
                return ApplicationResult(
                    "failed",
                    "Stopped before form interaction because the application page changed hosts.",
                )

            filled_fields = await self._fill_common_fields(page)
            if not is_trusted_job_url(page.url, job["link"], allow_trusted_ats=False):
                return ApplicationResult(
                    "failed",
                    "Stopped before resume upload because the application page changed hosts.",
                )

            await self._upload_resume(page)

            if self.submit:
                submitted = await self._click_submit(page)
                if submitted:
                    return ApplicationResult("submitted", f"Filled {filled_fields} fields and clicked submit.")

                return ApplicationResult(
                    "needs_manual_review",
                    f"Filled {filled_fields} fields, but no final submit button was found.",
                )

            return ApplicationResult(
                "ready_to_submit",
                f"Filled {filled_fields} fields in draft mode. Review the page before submitting.",
            )
        except PlaywrightTimeoutError as error:
            screenshot = await self._screenshot(page, job)
            return ApplicationResult("failed", f"Timed out: {error}. Screenshot: {screenshot}")
        except PlaywrightError as error:
            screenshot = await self._screenshot(page, job)
            return ApplicationResult("failed", f"Browser error: {error}. Screenshot: {screenshot}")

    async def _settle(self, page):
        try:
            await page.wait_for_load_state("networkidle", timeout=10000)
        except PlaywrightTimeoutError:
            pass

    async def _open_apply_flow(self, page):
        apply_controls = [
            page.get_by_role("link", name=self._regex(APPLY_TEXT)).first,
            page.get_by_role("button", name=self._regex(APPLY_TEXT)).first,
        ]

        for apply_control in apply_controls:
            try:
                await apply_control.wait_for(timeout=5000)
            except PlaywrightTimeoutError:
                continue

            try:
                async with page.context.expect_page(timeout=5000) as page_info:
                    await apply_control.click(timeout=5000)
                new_page = await page_info.value
                await new_page.wait_for_load_state("domcontentloaded")
                return new_page
            except PlaywrightTimeoutError:
                return page

        return page

    async def _fill_common_fields(self, page):
        fields = self.profile.get("fields", {})
        filled = 0

        for field_name, value in fields.items():
            if value in [None, ""]:
                continue

            control = page.get_by_label(self._label_regex(field_name)).first

            if await control.count() == 0:
                control = page.locator(
                    f"input[name*='{field_name}' i], textarea[name*='{field_name}' i]"
                ).first

            if await control.count() == 0:
                continue

            try:
                await control.fill(str(value), timeout=3000)
                filled += 1
            except PlaywrightError:
                continue

        return filled

    async def _upload_resume(self, page):
        resume_path = self.profile.get("resume_path")

        if not resume_path:
            return False

        path = Path(resume_path)
        allowed_root = Path(os.getenv("APPLICANT_DOCUMENTS_DIR", "artifacts")).resolve()

        if not path.is_file() or path.suffix.casefold() not in {".pdf", ".doc", ".docx"}:
            return False

        try:
            path.resolve().relative_to(allowed_root)
        except ValueError:
            return False

        if path.stat().st_size > 10 * 1024 * 1024:
            return False

        with path.open("rb") as resume_file:
            signature = resume_file.read(4)

        if path.suffix.casefold() == ".pdf" and signature != b"%PDF":
            return False
        if path.suffix.casefold() == ".doc" and signature != b"\xd0\xcf\x11\xe0":
            return False
        if path.suffix.casefold() == ".docx" and signature != b"PK\x03\x04":
            return False

        file_input = page.locator("input[type='file']").first

        if await file_input.count() == 0:
            return False

        await file_input.set_input_files(str(path))
        return True

    async def _click_submit(self, page):
        return False

    def _is_trusted_job(self, job):
        return any(
            site["company"] == job.get("company")
            and is_trusted_job_url(job.get("link", ""), site["url"], allow_trusted_ats=False)
            for site in sites
        )

    async def _screenshot(self, page, job):
        safe_title = "".join(char for char in job["title"][:60] if char.isalnum() or char in [" ", "-"]).strip()
        screenshot = self.screenshot_dir / f"{job['id']}-{safe_title or 'application'}.png"
        await page.screenshot(path=str(screenshot), full_page=True)
        return screenshot

    def _label_regex(self, field_name):
        readable = field_name.replace("_", " ")
        return self._regex(readable)

    def _regex(self, pattern) -> Pattern[str]:
        import re

        return re.compile(pattern, re.IGNORECASE)
