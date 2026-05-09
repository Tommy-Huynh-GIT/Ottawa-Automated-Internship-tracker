from selenium.webdriver.common.by import By

def generalScrapper(driver):
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