import pytest
import requests
import time
from data.urls import AUTH_REGISTER, AUTH_USER
from data.test_data import USER_NAMES, PASSWORDS


@pytest.fixture
def create_and_delete_user():
    """Фикстура для тестов логина (создаёт и удаляет пользователя)"""
    email = f"test_user_{int(time.time())}@yandex.ru"
    payload = {
        "email": email,
        "password": PASSWORDS["default"],
        "name": USER_NAMES["ivan"]
    }

    response = requests.post(AUTH_REGISTER, json=payload)
    token = response.json().get("accessToken")

    yield {"email": email, "password": PASSWORDS["default"], "name": USER_NAMES["ivan"], "token": token}

    # Удаляем пользователя после теста
    if token:
        requests.delete(AUTH_USER, headers={"Authorization": token})