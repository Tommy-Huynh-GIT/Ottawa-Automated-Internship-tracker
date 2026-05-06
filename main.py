from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

#Specifically Target Ottawa companies such as Kinaxis, Ciena, Ericcson, Ross Video, OXARA
#This holds list of carrer pages for companies in ottawa
urls = ["https://careers-kinaxis.icims.com/jobs/search?ss=1&searchKeyword=Intern&searchRelation=keyword_all",
       "https://solace.com/careers/",
       "https://ciena.wd5.myworkdayjobs.com/Careers?q=Intern&Location_Country=a30a87ed25634629aa6c3958aa2b91ea",
       "https://jobs.nokia.com/en/sites/CX_1/jobs?lastSelectedFacet=LOCATIONS&location=Ottawa%2C+Ontario%2C+Canada&locationId=100000018991137&locationLevel=city&mode=location&radius=25&radiusUnit=MI&selectedLocationsFacet=300000000471544&selectedTitlesFacet=TRA",
       "https://efds.fa.em5.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/jobs?lastSelectedFacet=LOCATIONS&location=Ottawa%2C+ON%2C+Canada&locationId=100000032213830&locationLevel=city&mode=location&radius=25&radiusUnit=MI&selectedLocationsFacet=300000000425151",
       "https://www.careers.ford.com/search-jobs/Developer/Ontario?orgIds=48560&kt=1&alp=6251999-6093943&alt=3",
       "https://gdmissionsystems.ca/careers/job-search?state=eyJhZGRyZXNzIjpbXSwiZmFjZXRzIjoiW3tcIm5hbWVcIjpcImNhcmVlcl9yYWRpdXNcIixcInZhbHVlc1wiOlt7XCJ2YWx1ZVwiOlwiNTAgbWlsZXNcIn1dfV0iLCJwYWdlIjowLCJ3aGVyZSI6Ik90dGF3YSwgT04iLCJsYXRpdHVkZSI6NDUuNDIwMjA0LCJsb25naXR1ZGUiOi03NS42OTc3OSwid2hhdCI6IkNvLU9wIiwicGFnZVNpemUiOjIwfQ%3D%3D",
       "https://www.shopify.com/careers?keyword=Intern#WhatWeDo",
       "https://ross-video.ttcportals.com/search/jobs?q=&location=Ottawa",
       "https://bb.wd3.myworkdayjobs.com/Student",
       "https://knak.com/careers/#current-openings"]

for url in urls:
    driver.get(url)

    time.sleep(3)

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