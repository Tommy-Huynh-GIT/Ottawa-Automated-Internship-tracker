from selenium import webdriver
from selenium.webdriver.common.by import By
#imported data set from sites.py
from sites import sites
from scrapers.general import generalScrapper
from scrapers.icims import icims
import time


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def oracle(driver):

    job_links = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
    
    keywords = ["intern", "co-op", "coop", "co-op/intern", "student"]

    for job in job_links:   

        text = job.text.strip().lower()
        link = job.get_attribute("href")

        if text and link:
            if any(k in text for k in keywords):
                print(job.text)
                print(link)
                print()