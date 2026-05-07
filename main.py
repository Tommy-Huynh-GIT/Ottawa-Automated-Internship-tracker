from selenium import webdriver
from selenium.webdriver.common.by import By
#imported data set from sites.py
from sites import sites
from scrapers.icims import icims
import time


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

#create specific kinaxis and nokia scrappers


#MAIN SCRAPPING CODE
for site in sites:

    #access the key-value pair
    company = site["company"]
    platform = site["platform"]
    url = site["url"]

    driver.get(url)

    time.sleep(3)
    


    #If the company is kinaxis run this scrapper
    #everything is in iframe 
    if company == "Kinaxis":

        icims(driver)
        
        #switch back to main page
        driver.switch_to.default_content()

        continue



    # Scroll so dynamic job listings can load on pages that render after the initial load
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #time.sleep(2)

    job_links = driver.find_elements(By.TAG_NAME, "a")

    keywords = ["intern", "co-op", "coop", "co-op/intern", "student"]

    for job in job_links:
        text = job.text.strip().lower()
        link = job.get_attribute("href")

        if text and link:
            if any(k in text for k in keywords):
                print(job.text)
                print(link)
                print()

time.sleep(5)



driver.quit()