import requests
import allure
import pytest
from data.urls import URL

class TestGetOrder:

    @pytest.mark.parametrize('color', [
        ['BLACK'],
        ['GREY'],
        ['BLACK', 'GRAY'],
        []
    ])
    @allure.title('Создать заказ')
    def test_get_order(self, color):

        payload = {
            "firstName": "Иван",
            "lastName": "Петров",
            "address": "Москва, Петровка, 15",
            "metroStation": 8,
            "phone": "+7 916 167 45 67",
            "rentTime": 2,
            "deliveryDate": "2025-06-06",
            "comment": "Привезите самокат",
            "color": color
        }

        r = requests.post(f"{URL}/api/v1/orders", json=payload)
        assert r.status_code == 201
        assert 'track' in r.json()