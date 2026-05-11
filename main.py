from selenium import webdriver
from selenium.webdriver.common.by import By
#imported data set from sites.py
from sites import sites
from scrapers.general import generalScrapper
from scrapers.icims import icims
from scrapers.oracle import oracle
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
    if platform == "ICIMS":

        icims(driver, company)
        
        #switch back to main page
        driver.switch_to.default_content()

        continue

    if platform == "Oracle":

        oracle(driver, company)

        continue




    # Scroll so dynamic job listings can load on pages that render after the initial load
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #time.sleep(2)
    generalScrapper(driver, company)

    

time.sleep(5)



driver.quit()