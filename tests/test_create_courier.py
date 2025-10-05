import requests
import allure
import pytest
from data.urls import URL
from data.courier_data import generation_new_courier_data
import logging


class TestCreateCourier:

    @allure.title('Создать курьера')
    def test_create_courier(self, delete_courier_data):
        data = generation_new_courier_data()
        data.pop("firstName")
        payload = data
        logging.info(f"Data for courier creation: {data}")

        with allure.step('Отправка запроса на создание курьера'):
            response = requests.post(f"{URL}/api/v1/courier", data=payload)

        with allure.step('Проверка статуса ответа на создание курьера'):
            assert response.status_code == 201, f"Failed to create courier: {response.status_code}"

        with allure.step('Проверка содержимого ответа'):
            assert response.json() == {'ok': True}, f"Unexpected response: {response.json()}"
        login_payload = {
            "login": payload["login"],
            "password": payload["password"]
        }

        with allure.step('Запрос на автортизацию курьера'):
            login_response = requests.post(f"{URL}/api/v1/courier/login", data=login_payload)

        with allure.step('Проверка статуса ответа на авторизацию курьера'):
            assert login_response.status_code == 200

        courier_id = login_response.json().get("id")

        with allure.step('Проверка ID курьера'):
            assert courier_id is not None,  "Courier ID should not be None."



    @allure.title('Нельзя создать дубль курьера')
    def test_create_courier_dubl_login(self, registered_courier_data):
        payload = registered_courier_data

        with allure.step('Отправка запроса на создание дубль курьера'):
            response = requests.post(f"{URL}/api/v1/courier", data=payload)

        with allure.step('Проверка статуса ответа на создание дубль курьера'):
            assert response.status_code == 409

        with allure.step('Проверка сообщения об ошибке'):
            assert "Этот логин уже используется" in response.json()["message"]

    @pytest.mark.parametrize('missing_field',['login','password'])
    @allure.title('Нельзя создать курьера, заполнены не все поля логин-пароль')
    def test_create_courier_with_missing_field(self, missing_field):
        data = generation_new_courier_data()
        payload = {
            "login": data["login"],
            "password": data["password"]
        }
        payload.pop(missing_field)

        with allure.step(f'Отправка запроса на создание курьера без заполнения логин-пароль: {missing_field}'):
            response = requests.post(f"{URL}/api/v1/courier", data=payload)

        with allure.step('Проверка статуса ответа не все поля логин-пароль заполнены'):
            assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"

        with allure.step('Проверка сообщения об ошибке'):
            assert "Недостаточно данных для создания учетной записи" in response.json()["message"], \
                f"Expected error message not found: {response.json()}"