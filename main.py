from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from spk import get_data
from sync import sync_data
import time, os

load_dotenv()

username = os.getenv("USER")
password = os.getenv("PASSWORD")
home_url = os.getenv("HOME_URL")
download_path = os.getenv("DOWNLOAD_PATH")

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

prefs = {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)

driver.get(home_url)
driver.find_element(By.NAME, "identity").send_keys(username)
driver.find_element(By.NAME, "password").send_keys(password)
driver.find_element(By.CSS_SELECTOR, ".home-button.button").click()

time.sleep(3)

get_data(driver, "Summary SPK", "Valid By Branch")

sync_data()

get_data(driver, "Summary RS", "By Branch")