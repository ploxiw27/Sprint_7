import requests
import pytest
import allure
from data.urls import URL
from data.courier_data import register_new_courier_and_return_login_password




class TestLoginCourier:
    @allure.title('Авторизация курьера')
    def test_login_courier(self, delete_courier_data):
        payload = delete_courier_data
        response = requests.post(f"{URL}/api/v1/courier/login", data=payload)

        assert response.status_code == 200
        assert 'id' in response.json()

    @allure.title('Авторизация не пройдена не существующий логин-пароль')
    def test_login_with_invalid_login_password(self):
        login_pass = register_new_courier_and_return_login_password()
        payload = {
            "login": login_pass[0],
            "password": login_pass[0]
        }
        response = requests.post(f"{URL}/api/v1/courier/login", data=payload)

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]


    @allure.title('Авторизация не пройдена не все обязательные поля заполнены')
    def test_login_courier_without_password(self):
        login_pass = register_new_courier_and_return_login_password()
        payload = {
            "login": login_pass[0],
            "password": ""
        }
        response = requests.post(f"{URL}/api/v1/courier/login", data=payload)

        assert response.status_code == 400
        assert "Недостаточно данных для входа" in response.json()["message"]