from selenium.webdriver.common.by import By
from datetime import datetime
from dotenv import load_dotenv
import time, os

load_dotenv()

download_path = os.getenv("DOWNLOAD_PATH")

def get_data(driver, menu, sub_menu):
    btn_menu = driver.find_element(By.XPATH, f"//span[text()='{menu}']")
    driver.execute_script("arguments[0].click();", btn_menu)

    btn_sub_menu = driver.find_element(By.XPATH, f"//span[text()='{menu}']/following::span[text()='{sub_menu}']")
    driver.execute_script("arguments[0].click();", btn_sub_menu)

    today = datetime.today().strftime("%Y-%m-%d")

    input_start_date = driver.find_element(By.NAME, "DateStart")
    driver.execute_script(
        """
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """,
        input_start_date,
        today,
    )

    input_end_date = driver.find_element(By.NAME, "DateEnd")
    driver.execute_script(
        """
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """,
        input_end_date,
        today,
    )

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    time.sleep(5)

    btn_export = driver.find_element(By.XPATH, "//button[text()='Export Table']")

    driver.execute_script("arguments[0].click();", btn_export)

    time.sleep(5)

    for f in os.listdir(download_path):
        if f.startswith("Laporan-Summary") and f.endswith(".xls"):
            if menu == "Summary SPK":
                new_name = "SPK.xls"
            elif menu == "Summary RS":
                new_name = "DO.xls"
            os.rename(os.path.join(download_path, f), os.path.join(download_path, new_name))
