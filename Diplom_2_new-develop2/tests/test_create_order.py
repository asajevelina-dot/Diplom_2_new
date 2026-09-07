import allure
import requests
import time
from data.urls import AUTH_REGISTER, ORDERS
from data.test_data import PASSWORDS, USER_NAMES, INGREDIENT_IDS
from data.error_messages import ErrorMessages


@allure.suite("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, create_and_delete_user):
        token = create_and_delete_user["token"]
        order_data = {
            "ingredients": INGREDIENT_IDS
        }

        with allure.step("Отправить запрос на создание заказа с авторизацией"):
            response = requests.post(
                ORDERS,
                json=order_data,
                headers={"Authorization": token}
            )

        with allure.step("Проверить код ответа 200"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert "order" in response.json()

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        order_data = {
            "ingredients": INGREDIENT_IDS
        }

        with allure.step("Отправить запрос на создание заказа без авторизации"):
            response = requests.post(ORDERS, json=order_data)

        with allure.step("Проверить код ответа 200"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_no_ingredients(self):
        with allure.step("Отправить запрос без ингредиентов"):
            response = requests.post(ORDERS, json={"ingredients": []})

        with allure.step("Проверить код ответа 400"):
            assert response.status_code == 400
            assert response.json()["message"] == ErrorMessages.INGREDIENT_IDS_REQUIRED

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredient_hash(self):
        order_data = {
            "ingredients": ["abc123def456", "xyz789ghi012"]
        }

        with allure.step("Отправить запрос с неверным хешем"):
            response = requests.post(ORDERS, json=order_data)

        with allure.step("Проверить код ответа 400"):
            assert response.status_code == 400