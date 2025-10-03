import requests
import random
import string
from data.urls import URL

def generation_new_courier_data():
    letters = string.ascii_lowercase
    login_new = ''.join(random.choice(letters) for i in range(8))
    password_new = ''.join(random.choice(letters) for i in range(10))
    first_name_new = ''.join(random.choice(letters) for i in range(8))

    return {"login": login_new, "password": password_new, "firstName": first_name_new}


def register_new_courier_and_return_login_password():

    login_pass = []

    data = generation_new_courier_data()
    login = data["login"]
    password = data["password"]
    first_name = data["firstName"]

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post(f"{URL}/api/v1/courier", data=payload)
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass