import requests
import allure
import pytest
import time

BASE_URL = "https://stellarburgers.education-services.ru/api"


@allure.suite("Логин пользователя")
class TestLoginUser:

    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user(self):
        email = f"ekaterina.vasilieva_{int(time.time())}@bk.ru"
        payload = {
            "email": email,
            "password": "CatLover2024",
            "name": "Екатерина Васильева"
        }
        requests.post(f"{BASE_URL}/auth/register", json=payload)
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": "CatLover2024"
        })
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Вход с неверным логином и паролем")
    @pytest.mark.parametrize("email,password", [
        ("dmitry.novikov@test.ru", "WrongPass123"),
        ("olga.sokolova@test.ru", "incorrect"),
        ("noname@test.ru", "qwerty"),
    ])
    def test_login_invalid_credentials(self, email, password):
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": password
        })
        assert response.status_code == 401
        assert response.json()["message"] == "email or password are incorrect"