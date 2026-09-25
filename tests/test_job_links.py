import unittest

from scrapers.links import (
    is_likely_job_link,
    is_trusted_job_url,
    normalize_job_link,
)


class JobLinkTests(unittest.TestCase):
    def test_keeps_absolute_http_links(self):
        link = "https://jobs.example.com/intern/123#details"

        self.assertEqual(
            normalize_job_link(link, "https://jobs.example.com/search"),
            "https://jobs.example.com/intern/123#details",
        )

    def test_rejects_insecure_or_external_hosts(self):
        source_url = "https://careers.example.com/search"

        self.assertIsNone(normalize_job_link("http://careers.example.com/job/123", source_url))
        self.assertIsNone(normalize_job_link("//attacker.example/jobs/123", source_url))
        self.assertIsNone(normalize_job_link("https://attacker.example/jobs/123", source_url))
        self.assertIsNone(normalize_job_link("https://user:pass@careers.example.com/job/123", source_url))

    def test_allows_known_ats_hosts(self):
        source_url = "https://careers.example.com/search"

        self.assertEqual(
            normalize_job_link("https://jobs.lever.co/example/123", source_url),
            "https://jobs.lever.co/example/123",
        )

    def test_rejects_untrusted_redirect_destinations(self):
        source_url = "https://careers.example.com/job/123"

        self.assertTrue(is_trusted_job_url(source_url, source_url))
        self.assertTrue(is_trusted_job_url("https://jobs.lever.co/example/123", source_url))
        self.assertTrue(is_trusted_job_url("https://company.greenhouse.io/example/123", source_url))
        self.assertTrue(is_trusted_job_url("https://company.myworkdayjobs.com/example/123", source_url))
        self.assertFalse(
            is_trusted_job_url("https://jobs.lever.co/example/123", source_url, allow_trusted_ats=False)
        )
        self.assertFalse(is_trusted_job_url("https://attacker.example/job/123", source_url))

    def test_resolves_relative_links_against_source_page(self):
        self.assertEqual(
            normalize_job_link("/jobs/123", "https://example.com/careers/"),
            "https://example.com/jobs/123",
        )
        self.assertEqual(
            normalize_job_link("job/123", "https://example.com/careers/"),
            "https://example.com/careers/job/123",
        )

    def test_identifies_job_detail_links(self):
        self.assertTrue(is_likely_job_link("https://example.com/jobs/123"))
        self.assertTrue(is_likely_job_link("https://example.com/career/software-intern"))
        self.assertTrue(is_likely_job_link("https://example.com/careers/software-intern"))
        self.assertTrue(is_likely_job_link("https://jobs.lever.co/example/123"))
        self.assertTrue(is_likely_job_link("https://jobs.ashbyhq.com/example/123"))
        self.assertTrue(is_likely_job_link("https://careers.smartrecruiters.com/example/123"))
        self.assertFalse(is_likely_job_link("https://example.com/student-loans"))

    def test_rejects_non_web_links(self):
        source_url = "https://example.com/careers/"

        for link in (
            None,
            "",
            "   ",
            "#details",
            "javascript:void(0)",
            "mailto:jobs@example.com",
        ):
            with self.subTest(link=link):
                self.assertIsNone(normalize_job_link(link, source_url))


if __name__ == "__main__":
    unittest.main()