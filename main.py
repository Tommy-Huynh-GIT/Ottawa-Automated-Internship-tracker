from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

#create specific kinaxis and nokia scrappers


#Specifically Target Ottawa companies such as Kinaxis, Ciena, Ericcson, Ross Video, OXARA
#Stores key value pairs
#This holds list of carrer pages for companies in ottawa
sites = [
    {
        "company": "Kinaxis",
        "platform": "ICIMS",
        "url": "https://careers-kinaxis.icims.com/jobs/search?ss=1&searchKeyword=Intern&searchRelation=keyword_all"
    },

    {
        "company": "Solace",
        "platform": "Custom",
        "url": "https://solace.com/careers/"
    },

    {
        "company": "Ciena",
        "platform": "Workday",
        "url": "https://ciena.wd5.myworkdayjobs.com/Careers?q=Intern&Location_Country=a30a87ed25634629aa6c3958aa2b91ea"
    },

    {
        "company": "Nokia",
        "platform": "Oracle",
        "url": "https://jobs.nokia.com/en/sites/CX_1/jobs?lastSelectedFacet=LOCATIONS&location=Ottawa%2C+Ontario%2C+Canada&locationId=100000018991137&locationLevel=city&mode=location&radius=25&radiusUnit=MI&selectedLocationsFacet=300000000471544&selectedTitlesFacet=TRA"
    },

    {
        "company": "Ross Video",
        "platform": "Oracle",
        "url": "https://efds.fa.em5.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/jobs?lastSelectedFacet=LOCATIONS&location=Ottawa%2C+ON%2C+Canada&locationId=100000032213830&locationLevel=city&mode=location&radius=25&radiusUnit=MI&selectedLocationsFacet=300000000425151"
    },

    {
        "company": "Ford",
        "platform": "Custom",
        "url": "https://www.careers.ford.com/search-jobs/Developer/Ontario?orgIds=48560&kt=1&alp=6251999-6093943&alt=3"
    },

    {
        "company": "General Dynamics",
        "platform": "Custom",
        "url": "https://gdmissionsystems.ca/careers/job-search?state=eyJhZGRyZXNzIjpbXSwiZmFjZXRzIjoiW3tcIm5hbWVcIjpcImNhcmVlcl9yYWRpdXNcIixcInZhbHVlc1wiOlt7XCJ2YWx1ZVwiOlwiNTAgbWlsZXNcIn1dfV0iLCJwYWdlIjowLCJ3aGVyZSI6Ik90dGF3YSwgT04iLCJsYXRpdHVkZSI6NDUuNDIwMjA0LCJsb25naXR1ZGUiOi03NS42OTc3OSwid2hhdCI6IkNvLU9wIiwicGFnZVNpemUiOjIwfQ%3D%3D"
    },

    {
        "company": "Shopify",
        "platform": "Custom",
        "url": "https://www.shopify.com/careers?keyword=Intern#WhatWeDo"
    },

    {
        "company": "Ross Video TTC",
        "platform": "Custom",
        "url": "https://ross-video.ttcportals.com/search/jobs?q=&location=Ottawa"
    },

    {
        "company": "BlackBerry",
        "platform": "Workday",
        "url": "https://bb.wd3.myworkdayjobs.com/Student"
    },

    {
        "company": "Knak",
        "platform": "Custom",
        "url": "https://knak.com/careers/#current-openings"
    }
]

#GENERIC SCRAPER
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

        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "icims_content_iframe"))
        )

        driver.switch_to.frame(iframe)

        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )

        job_links = driver.find_elements(
            By.CSS_SELECTOR,
            "a[href*='/jobs/'][href*='/job']"
        )

        print("Kinaxis jobs found:", len(job_links))

        for job in job_links:
            title = job.text.strip()
            link = job.get_attribute("href")

            if title:
                print(title)
                print(link)
                print()

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