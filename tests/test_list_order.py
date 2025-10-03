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

        requests.post(f"{URL}/api/v1/orders", json=payload)
        r = requests.get(f"{URL}/api/v1/orders")
        assert r.status_code == 200
        assert 'orders' in r.json()