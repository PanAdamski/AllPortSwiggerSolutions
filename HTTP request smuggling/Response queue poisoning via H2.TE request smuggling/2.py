import socket
import ssl
import certifi
import h2.connection
import h2.events
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

    # Rozdzielenie URL na nazwę hosta
    burp_url = sys.argv[1]
    host_burp = burp_url[8:]  # Usuwamy "https://"
    
    # Konfiguracja gniazda i SSL
    socket.setdefaulttimeout(15)
    ctx = ssl.create_default_context(cafile=certifi.where())
    ctx.set_alpn_protocols(['h2'])

    # Otwarcie gniazda do serwera i inicjowanie SSL
    s = socket.create_connection((host_burp, 443))
    s = ctx.wrap_socket(s, server_hostname=host_burp)

    # Utworzenie połączenia H2
    c = h2.connection.H2Connection()
    c.initiate_connection()
    s.sendall(c.data_to_send())

    # Wysyłanie zapytania POST
    headers = [
        (':method', 'POST'),
        (':path', '/'),
        (':authority', host_burp),
        (':scheme', 'https'),
        ('Transfer-Encoding', 'chunked'),
    ]
    c.send_headers(stream_id=1, headers=headers, end_stream=False)
    s.sendall(c.data_to_send())

    # Wysłanie pustego chunku (0)
    s.sendall(b'0\r\n\r\n')

    # Wysyłanie zapytania GET
    headers_get = [
        (':method', 'GET'),
        (':path', '/x'),  # Możesz zmienić tę ścieżkę na inną, np. '/'
        (':authority', host_burp),
        (':scheme', 'https'),
    ]
    print("Wysyłam zapytanie GET /x")
    c.send_headers(stream_id=3, headers=headers_get, end_stream=True)
    s.sendall(c.data_to_send())
    print("Zapytanie wysłane. Oczekiwanie na odpowiedź...")

    body = b''
    response_stream_ended = False
    while not response_stream_ended:
        # Odbieranie surowych danych z gniazda
        data = s.recv(65536)
        if not data:
            break
        
        print("Odebrano surowe dane:", repr(data))  # Debugging line

        # Przesyłanie surowych danych do h2 i przetwarzanie zdarzeń
        events = c.receive_data(data)
        for event in events:
            if isinstance(event, h2.events.DataReceived):
                c.acknowledge_received_data(event.flow_controlled_length, event.stream_id)
                body += event.data
            if isinstance(event, h2.events.StreamEnded):
                response_stream_ended = True

        # Wysłanie wszelkich oczekujących danych do serwera
        s.sendall(c.data_to_send())

    print("Odebrano odpowiedź w całości:")
    print(body)  # Wyświetlenie odpowiedzi
    print("Odebrano odpowiedź w hex:")
    print(body.hex())
    # Zamknięcie połączenia H2
    c.close_connection()
    s.sendall(c.data_to_send())

    # Zamknięcie gniazda
    s.close()
