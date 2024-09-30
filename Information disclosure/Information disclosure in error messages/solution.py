import requests
import sys
import re

burp_url = sys.argv[1]
error_url = burp_url + '/product?productId=e'
answer_url = burp_url + '/submitSolution'

r = requests.get(error_url)
response = r.text

pattern = r'Apache Struts 2 (\d+\.\d+\.\d+)'
match = re.search(pattern, response)

version = match.group(1)

requests.post(answer_url, data={"answer": version})
