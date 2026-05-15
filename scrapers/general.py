from selenium.webdriver.common.by import By
from constants import KEYWORDS
from database.postgres import save_job


def generalScrapper(driver, company):
    print(f"NOW SCRAPING {company}!")
    print("====================================")

    if(company == "General Dynamics"):
        #anchor tags that hold the right links don't have classes
        job_links = driver.find_elements(By.CSS_SELECTOR, "a:not([class])")
        
    else:
        job_links = driver.find_elements(By.TAG_NAME, "a")

    for job in job_links:
        title = job.text.strip().lower()
        link = job.get_attribute("href")

        if title and link:
            if KEYWORDS.search(title):
                #Push to database
                save_job(link, title, company)