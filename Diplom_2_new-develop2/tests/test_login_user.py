import allure
import pytest
import requests
from data.urls import AUTH_LOGIN
from data.test_data import PASSWORDS


@allure.suite("Логин пользователя")
class TestLoginUser:

    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user(self, create_and_delete_user):
        email = create_and_delete_user["email"]

        with allure.step("Отправить запрос на логин"):
            response = requests.post(AUTH_LOGIN, json={
                "email": email,
                "password": PASSWORDS["default"]
            })

        with allure.step("Проверить код ответа и наличие токена"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert "accessToken" in response.json()

    @allure.title("Вход с неверным логином и паролем")
    @pytest.mark.parametrize("email,password", [
        ("dmitry.novikov@test.ru", "WrongPass123"),
        ("olga.sokolova@test.ru", "incorrect"),
        ("noname@test.ru", "qwerty"),
    ])
    def test_login_invalid_credentials(self, email, password):
        with allure.step("Отправить запрос с неверными данными"):
            response = requests.post(AUTH_LOGIN, json={
                "email": email,
                "password": password
            })

        with allure.step("Проверить код ответа 401"):
            assert response.status_code == 401
            assert response.json()["message"] == "email or password are incorrect"