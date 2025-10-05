import requests
import allure
from data.urls import URL

class TestListOrder:


    @allure.title('Получение списка заказов')
    def test_list_order(self):

        payload = {
            "firstName": "Иван",
            "lastName": "Петров",
            "address": "Москва, Петровка, 15",
            "metroStation": 8,
            "phone": "+7 916 167 45 67",
            "rentTime": 2,
            "deliveryDate": "2025-06-06",
            "comment": "Привезите самокат",
            "color": "BLACK"
        }

        with allure.step('Отправка запроса на создание заказа'):
            requests.post(f"{URL}/api/v1/orders", json=payload)

        with allure.step('Отправка запроса на получение списка заказов'):
            response = requests.get(f"{URL}/api/v1/orders")

        with allure.step('Проверка статуса на получение списка заказов'):
            assert response.status_code == 200, f'Failed to get orders:{response.status_code}'

        with allure.step('Проверка на присутствие ключа orders'):
            assert 'orders' in response.json()