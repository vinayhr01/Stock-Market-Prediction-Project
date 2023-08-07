import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re
import os

def download_csv():
    userSearch = input("Give the name to get stock price prediction \n")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")  # Removes INFO logging in the terminal
    download_directory = os.path.join(os.getcwd(), "CSV Files")
    chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://finance.yahoo.com")
    search = driver.find_element(By.CSS_SELECTOR, "input#yfin-usr-qry")
    search.send_keys(userSearch)
    search.send_keys(Keys.RETURN)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_changes(driver.current_url))
    newUrl = driver.current_url

    AnDriver = webdriver.Chrome(options=chrome_options)
    AnDriver.get(newUrl)

    hist_data = AnDriver.find_element(By.XPATH, '//li[@data-test="HISTORICAL_DATA"]/a')
    hist_data.click()

    h1_element = AnDriver.find_element(By.XPATH, '//h1[contains(@class, "D(ib) Fz(18px)")]').text

    time.sleep(5)

    download = AnDriver.find_element(By.XPATH, '//span[text()="Download"]')
    download_link = download.find_element(By.XPATH, './..')
    download_link.click()

    time.sleep(15)

    pattern = r'\((.*?)\)'  # Matches text within parentheses
    matches = re.search(pattern, h1_element)

    extracted_text = matches.group(1)

    filename = extracted_text+".csv"

    data = pd.read_csv(".\\CSV Files\\"+filename)

    data['Stock'] = h1_element

    data.to_csv(".\\CSV Files\\"+filename, index=False)

    driver.quit()