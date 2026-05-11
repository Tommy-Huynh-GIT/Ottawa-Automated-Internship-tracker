from selenium.webdriver.common.by import By
from constants import KEYWORDS


def generalScrapper(driver):
    job_links = driver.find_elements(By.TAG_NAME, "a")

    for job in job_links:
        text = job.text.strip().lower()
        link = job.get_attribute("href")

        if text and link:
            if any(k in text for k in KEYWORDS):
                print(job.text)
                print(link)
                print()