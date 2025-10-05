import requests
import pytest
import allure
from data.urls import URL
from data.courier_data import register_new_courier_and_return_login_password


class TestLoginCourier:
    @allure.title('Авторизация курьера')
    def test_login_courier(self, delete_courier_data):
        payload = delete_courier_data

        with allure.step('Запрос на авторизацию курьера'):
            response = requests.post(f"{URL}/api/v1/courier/login", data=payload)

        with allure.step('Проверка статуса на авторизацию курьера'):
            assert response.status_code == 200

        with allure.step('Проверка на присутсвие ID курьера'):
            assert 'id' in response.json()

    @allure.title('Авторизация не пройдена не существующий логин-пароль')
    def test_login_with_invalid_login_password(self):
        login_pass = register_new_courier_and_return_login_password()
        payload = {
            "login": login_pass[0],
            "password": login_pass[0]
        }

        with allure.step('Отправка запроса на авторизацию не существующий логин-пароль'):
            response = requests.post(f"{URL}/api/v1/courier/login", data=payload)

        with allure.step('Просверк статуса ответа на неверный логин-пароль'):
            assert response.status_code == 404

        with allure.step('Проверка сообщения об ошибке на неверный логин-пароль'):
            assert "Учетная запись не найдена" in response.json()["message"]


    @allure.title('Авторизация не пройдена не все обязательные поля заполнены')
    def test_login_courier_without_password(self):
        login_pass = register_new_courier_and_return_login_password()
        payload = {
            "login": login_pass[0],
            "password": ""
        }

        with allure.step('Отправка запроса на авторизацию не заполнен логин-пароль'):
            response = requests.post(f"{URL}/api/v1/courier/login", data=payload)

        with allure.step('Проверка статуса ответа на запрос не заполнены все поля'):
            assert response.status_code == 400

        with allure.step('Проверка сообщение об ошиьке на не заполнены все поля'):
            assert "Недостаточно данных для входа" in response.json()["message"]