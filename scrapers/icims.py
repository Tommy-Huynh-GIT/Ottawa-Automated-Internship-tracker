from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def icims(driver):
        
      #load iframe first, check for 20 seconds until it exists
        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "icims_content_iframe"))
        )

        #switch to iframe from main page
        driver.switch_to.frame(iframe)

        #wait until all anchor tags exist inside the iframe
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )

        #find all elements with /jobs/ or /job/ in the link
        job_links = driver.find_elements(
            By.CSS_SELECTOR,
            "a[href*='/jobs/'][href*='/job']"
        )

        print("Kinaxis jobs found:", len(job_links))

        keywords = ["intern", "co-op/intern", "co-op", "coop"]


        #loop through job links
        for job in job_links:
            #replace title with blank space and remove any trailing space, new line
            title = job.text.replace("Title", "").strip()
            link = job.get_attribute("href")

            #use this for the print
            title_lower = title.lower()

            if any(keyword in title_lower for keyword in keywords):
                print(title)
                print(link)
                print()
