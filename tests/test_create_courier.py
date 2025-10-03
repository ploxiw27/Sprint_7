import requests
import allure
import pytest
from data.urls import URL
from data.courier_data import generation_new_courier_data
from data.courier_data import register_new_courier_and_return_login_password
import logging


class TestCreateCourier:

    @allure.title('Создать курьера')
    def test_create_courier(self, registered_courier_data):
        data = generation_new_courier_data()
        data.pop("firstName")
        payload = data
        logging.info(f"Data for courier creation: {data}")
        print(data)

        response = requests.post(f"{URL}/api/v1/courier", data=payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

        login_payload = {
            "login": payload["login"],
            "password": payload["password"]
        }
        login_response = requests.post(f"{URL}/api/v1/courier/login", data=login_payload)
        assert login_response.status_code == 200

        courier_id = login_response.json().get("id")
        assert courier_id is not None

        delete_response = requests.delete(f"{URL}/api/v1/courier/{courier_id}")
        assert delete_response.status_code == 200


    @allure.title('Нельзя создать дубль курьера')
    def test_create_courier_dubl_login(self, registered_courier_data):
        payload = registered_courier_data
        response = requests.post(f"{URL}/api/v1/courier", data=payload)

        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json()["message"]


    @allure.title('Нельзя создать курьера, заполнены не все поля')
    def test_create_courier_without_password(self):
        data = generation_new_courier_data()
        payload = {
            "login": data["login"],
            "firstName": data["firstName"]
        }
        response = requests.post(f"{URL}/api/v1/courier", data=payload)

        assert response.status_code == 400
        assert "Недостаточно данных для создания учетной записи" in response.json()["message"]