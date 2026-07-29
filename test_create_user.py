import requests
import allure
import pytest
import time

BASE_URL = "https://stellarburgers.education-services.ru/api"


@allure.suite("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self):
        email = f"ivan.petrov_{int(time.time())}@yandex.ru"
        payload = {
            "email": email,
            "password": "SecurePass123",
            "name": "Иван Петров"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self):
        email = f"anna.smirnova_{int(time.time())}@mail.ru"
        payload = {
            "email": email,
            "password": "MyPassword456",
            "name": "Анна Смирнова"
        }
        requests.post(f"{BASE_URL}/auth/register", json=payload)
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, missing_field):
        payload = {
            "email": f"alexey.kozlov_{int(time.time())}@gmail.com",
            "password": "Qwerty789",
            "name": "Алексей Козлов"
        }
        del payload[missing_field]
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"