import requests
import allure
import time

BASE_URL = "https://stellarburgers.education-services.ru/api"


@allure.suite("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self):
        email = f"mikhail.ivanov_{int(time.time())}@rambler.ru"
        user_data = {
            "email": email,
            "password": "BurgerLover99",
            "name": "Михаил Иванов"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        token = response.json()["accessToken"]
        order_data = {
            "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
        }
        response = requests.post(
            f"{BASE_URL}/orders",
            json=order_data,
            headers={"Authorization": token}
        )
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        order_data = {
            "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
        }
        response = requests.post(f"{BASE_URL}/orders", json=order_data)
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_no_ingredients(self):
        response = requests.post(f"{BASE_URL}/orders", json={"ingredients": []})
        assert response.status_code == 400
        assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredient_hash(self):
        order_data = {
            "ingredients": ["abc123def456", "xyz789ghi012"]
        }
        response = requests.post(f"{BASE_URL}/orders", json=order_data)
        assert response.status_code == 400