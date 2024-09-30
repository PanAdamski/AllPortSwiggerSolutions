import requests

burp0_url = "https://0aae00780385e3d9822b2461005b00d0.web-security-academy.net:443/product/stock"
burp0_cookies = {"session": "WoxcToawXid9Y5B0Mae5QPBvRCd468JZ"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0", "Accept": "*/*", "Accept-Language": "pl,en-US;q=0.7,en;q=0.3", "Accept-Encoding": "gzip, deflate, br", "Referer": "https://0aae00780385e3d9822b2461005b00d0.web-security-academy.net/product?productId=3", "Content-Type": "application/xml", "Origin": "https://0aae00780385e3d9822b2461005b00d0.web-security-academy.net", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Priority": "u=0", "Te": "trailers"}
burp0_data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><stockCheck><productId>3</productId><storeId>1</storeId></stockCheck>"
r = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
print(r.text)
