import pytest
import requests
from data.urls import URL
from data.courier_data import register_new_courier_and_return_login_password

@pytest.fixture
def registered_courier_data():
    login_pass = register_new_courier_and_return_login_password()
    return {
        "login": login_pass[0],
        "password": login_pass[1],
        "firstName": login_pass[2]
    }

@pytest.fixture
def delete_courier_data():
    login_pass = register_new_courier_and_return_login_password()
    courier_payload = {
        "login": login_pass[0],
        "password": login_pass[1]
    }
    response = requests.post(f"{URL}/api/v1/courier/login", data=courier_payload)

    assert response.status_code == 200
    courier_id = response.json()["id"]
    assert courier_id is not None

    yield courier_payload

    delete_response = requests.delete(f'{URL}/api/v1/courier/{courier_id}')
    assert delete_response.status_code ==  200, f"Failed to delete courier. Status code: {delete_response.status_code}"