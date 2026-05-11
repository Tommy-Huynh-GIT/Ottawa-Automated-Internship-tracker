from selenium import webdriver
from selenium.webdriver.common.by import By
#imported data set from sites.py
from sites import sites
from scrapers.general import generalScrapper
from scrapers.icims import icims



from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def oracle(driver, company):

    if company == "Nokia":

        #wait for all links
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "a.job-grid-item__link")
            )
        )

        job_links = driver.find_elements(
            By.CSS_SELECTOR,
            "a.job-grid-item__link"
        )

        for job in job_links:

            #this gives us an id to find an element that has the text, 
            labelled_by = job.get_attribute("aria-labelledby")
            #This element holds the text for the current job
            title_element = driver.find_element(By.ID, labelled_by)

            title = title_element.text.strip()
            link = job.get_attribute("href")

            if title and link:
                print(title)
                print(link)
                print()
            

            

   