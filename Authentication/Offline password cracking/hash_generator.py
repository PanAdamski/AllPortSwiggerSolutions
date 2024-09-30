import hashlib

input_file = '../Portswigger_lists/password_list.txt'
output_file = 'hashed_passwords.txt'

def hash_password(password):
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    return md5_hash

with open(input_file, 'r') as infile:
    passwords = infile.readlines()

with open(output_file, 'w') as outfile:
    for password in passwords:
        password = password.strip()  
        hashed_password = hash_password(password)
        outfile.write(f'{hashed_password}:{password}\n')
