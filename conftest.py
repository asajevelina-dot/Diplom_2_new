import pytest
import requests
import time

BASE_URL = "https://stellarburgers.education-services.ru/api"


@pytest.fixture
def create_user():
    email = f"test_user_{int(time.time())}@yandex.ru"
    password = "TestPass123"
    name = "Тестовый пользователь"

    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    token = response.json().get("accessToken")

    yield {"email": email, "password": password, "name": name, "token": token}