import socket
import ssl


def connect_h2_socket(host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    context.set_alpn_protocols(["h2"])
    sock.connect((host, 443))
    sock = context.wrap_socket(sock, server_hostname=host)
    return sock



s = connect_h2_socket("0ad3000304e2eb6889ca2c4600020065.web-security-academy.net")
print("Selected protocol:", s.selected_alpn_protocol())
print(s.recv(4096).decode())
