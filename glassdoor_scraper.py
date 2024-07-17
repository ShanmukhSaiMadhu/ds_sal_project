from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    options = webdriver.ChromeOptions()
    # Uncomment the line below if you'd like to run Chrome headless
    # options.add_argument('headless')
    
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url = f'https://www.glassdoor.com/Job/index.htm'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:

        time.sleep(slp_time)

        try:
            driver.find_element(By.XPATH, './/button[text()="Accept All"]').click()
        except ElementClickInterceptedException:
            pass

        job_buttons = driver.find_elements(By.XPATH, './/li[@data-test="jobListing"]')
        for job_button in job_buttons:

            print(f"Progress: {len(jobs)}/{num_jobs}")
            if len(jobs) >= num_jobs:
                break

            job_button.click()
            time.sleep(1)
            collected_successfully = False

            while not collected_successfully:
                try:
                    company_name = driver.find_element(By.XPATH, './/div[@data-test="job-info"]/div[@class="employerName"]').text
                    location = driver.find_element(By.XPATH, './/div[@data-test="job-info"]/div[@class="jobEmpolyerLocation"]').text
                    job_title = driver.find_element(By.XPATH, './/div[@data-test="job-info"]/div[@class="jobLink jobInfoItem jobTitle"]').text
                    job_description = driver.find_element(By.XPATH, './/div[@data-test="job-info"]/div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element(By.XPATH, './/span[@class="gray small salary"]').text
            except NoSuchElementException:
                salary_estimate = -1

            try:
                rating = driver.find_element(By.XPATH, './/span[@class="css-1m5m32b e1tk4kwz1"]').text
            except NoSuchElementException:
                rating = -1

            if verbose:
                print(f"Job Title: {job_title}")
                print(f"Salary Estimate: {salary_estimate}")
                print(f"Job Description: {job_description[:500]}")
                print(f"Rating: {rating}")
                print(f"Company Name: {company_name}")
                print(f"Location: {location}")

            jobs.append({
                "Job Title": job_title,
                "Salary Estimate": salary_estimate,
                "Job Description": job_description,
                "Rating": rating,
                "Company Name": company_name,
                "Location": location,
            })

        try:
            driver.find_element(By.XPATH, './/li[@class="next"]//a').click()
        except NoSuchElementException:
            print(f"Scraping terminated before reaching target number of jobs. Needed {num_jobs}, got {len(jobs)}.")
            break

    return pd.DataFrame(jobs)

if __name__ == "__main__":
    path_to_chromedriver = 'D:/path/to/chromedriver'  # Replace with your path to chromedriver
    keyword = 'data scientist'  # Specify the job title or keyword you want to search for
    num_jobs = 15  # Specify the number of jobs you want to scrape
    verbose = True  # Set to True to print detailed progress and job information
    slp_time = 5  # Adjust sleep time based on your internet speed

    df = get_jobs(keyword, num_jobs, verbose, path_to_chromedriver, slp_time)
    print(df.head())
