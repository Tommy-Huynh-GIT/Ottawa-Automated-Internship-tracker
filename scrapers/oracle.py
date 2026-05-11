from selenium import webdriver
from selenium.webdriver.common.by import By
#imported data set from sites.py
from sites import sites
from scrapers.general import generalScrapper
from scrapers.icims import icims
import time


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def oracle(driver, company):

    if company == "Nokia":

        #wait for links
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "a.job-grid-item__link")
            )
        )

        #grab job links
        job_links = driver.find_elements(By.CSS_SELECTOR, "a.job-grid-item__link")

        for job in job_links:
            #parent
            title = WebDriverWait(driver,20).until(EC.presence_of_element_located(By.CLASS_NAME, "div.job-grid-item__link"))

            link = job.get_attribute("href")

            if title and link:
                


            

            

   