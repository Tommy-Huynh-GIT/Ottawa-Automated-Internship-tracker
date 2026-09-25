import unittest
from urllib.parse import urlparse

from main import SCRAPERS
from sites import sites


EXPECTED_NEW_COMPANIES = {
    "Ericsson",
    "MDA Space",
    "Telesat",
    "Calian",
    "ADGA Group",
    "Thales Canada",
    "Lockheed Martin Canada",
    "Mitel",
    "March Networks",
    "N-able",
    "Assent",
    "Fullscript",
    "Bluink",
    "Trend Micro",
    "QNX",
    "Ottawa Hospital Research Institute",
    "National Research Council Canada",
    "Communications Security Establishment",
    "TrendAI",
}

EXPECTED_KANATA_COMPANIES = {
    "Ranovus",
    "ThinkRF",
    "Juniper Networks",
    "Wind River",
    "Ribbon Communications",
    "Skyworks Solutions",
    "Semtech",
    "Microchip Technology",
    "Synopsys",
    "Keysight Technologies",
    "Amdocs",
    "Pythian",
    "L3Harris Technologies",
    "Kongsberg Geospatial",
}


class SiteConfigurationTests(unittest.TestCase):
    def test_requested_ottawa_companies_are_configured(self):
        configured_companies = {site["company"] for site in sites}

        self.assertTrue(EXPECTED_NEW_COMPANIES <= configured_companies)

    def test_kanata_tech_companies_are_configured(self):
        configured_sites = {site["company"]: site for site in sites}

        self.assertTrue(EXPECTED_KANATA_COMPANIES <= configured_sites.keys())
        for company in EXPECTED_KANATA_COMPANIES:
            self.assertEqual(configured_sites[company]["location_keywords"], ["Ottawa", "Kanata"])

    def test_site_entries_are_unique_and_complete(self):
        company_names = [site["company"].casefold() for site in sites]
        source_urls = [site["url"].rstrip("/") for site in sites]

        self.assertEqual(len(company_names), len(set(company_names)))
        self.assertEqual(len(source_urls), len(set(source_urls)))

        for site in sites:
            self.assertTrue({"company", "platform", "url"} <= set(site))
            parsed_url = urlparse(site["url"])
            self.assertIn(parsed_url.scheme, {"http", "https"})
            self.assertTrue(parsed_url.netloc)

    def test_every_configured_platform_has_an_explicit_scraper(self):
        self.assertTrue({site["platform"] for site in sites} <= set(SCRAPERS))


if __name__ == "__main__":
    unittest.main()