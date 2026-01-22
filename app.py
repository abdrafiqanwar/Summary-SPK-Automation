from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv
from datetime import datetime
import os, time

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
wait = WebDriverWait(driver, 5)

driver.get(home_url)
driver.find_element(By.NAME, "identity").send_keys(username)
driver.find_element(By.NAME, "password").send_keys(password)
driver.find_element(By.CSS_SELECTOR, ".home-button.button").click()

time.sleep(3)

btn_report = driver.find_element(By.XPATH, "//span[text()='Summary SPK']")
driver.execute_script("arguments[0].click();", btn_report)

btn_sales = driver.find_element(By.XPATH, "//span[text()='Summary SPK']/following::span[text()='Valid By Branch']")
driver.execute_script("arguments[0].click();", btn_sales)

today = datetime.today().strftime("%Y-%m-%d")

date_start_input = driver.find_element(By.NAME, "DateStart")
driver.execute_script(
    """
    arguments[0].value = arguments[1];
    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """,
    date_start_input,
    today,
)

date_end_input = driver.find_element(By.NAME, "DateEnd")
driver.execute_script(
    """
    arguments[0].value = arguments[1];
    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """,
    date_end_input,
    today,
)

driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

time.sleep(5)

export_btn = driver.find_element(By.XPATH, "//button[text()='Export Table']")

driver.execute_script("arguments[0].click();", export_btn)

time.sleep(10)

driver.quit()
