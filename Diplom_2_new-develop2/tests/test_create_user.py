import allure
import pytest
import requests
import time
from data.urls import AUTH_REGISTER, AUTH_USER
from data.test_data import USER_NAMES, PASSWORDS


@allure.suite("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self):
        email = f"ivan.petrov_{int(time.time())}@yandex.ru"
        payload = {
            "email": email,
            "password": PASSWORDS["secure"],
            "name": USER_NAMES["ivan"]
        }

        with allure.step("Отправить запрос на регистрацию"):
            response = requests.post(AUTH_REGISTER, json=payload)

        with allure.step("Проверить код ответа и данные пользователя"):
            assert response.status_code == 200
            assert response.json()["success"] is True

        # ✅ УДАЛЯЕМ ПОЛЬЗОВАТЕЛЯ ПОСЛЕ ТЕСТА
        token = response.json().get("accessToken")
        if token:
            with allure.step("Удалить созданного пользователя"):
                requests.delete(AUTH_USER, headers={"Authorization": token})

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self):
        email = f"anna.smirnova_{int(time.time())}@mail.ru"
        payload = {
            "email": email,
            "password": PASSWORDS["mypassword"],
            "name": USER_NAMES["anna"]
        }

        with allure.step("Создать пользователя"):
            response_first = requests.post(AUTH_REGISTER, json=payload)
            token = response_first.json().get("accessToken")

        with allure.step("Попробовать зарегистрироваться повторно"):
            response = requests.post(AUTH_REGISTER, json=payload)

        with allure.step("Проверить код ответа 403"):
            assert response.status_code == 403
            assert response.json()["message"] == "User already exists"

        # ✅ УДАЛЯЕМ ПОЛЬЗОВАТЕЛЯ ПОСЛЕ ТЕСТА
        if token:
            with allure.step("Удалить созданного пользователя"):
                requests.delete(AUTH_USER, headers={"Authorization": token})

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, missing_field):
        email = f"alexey.kozlov_{int(time.time())}@gmail.com"
        payload = {
            "email": email,
            "password": PASSWORDS["default"],
            "name": USER_NAMES["alexey"]
        }
        del payload[missing_field]

        with allure.step(f"Отправить запрос без поля {missing_field}"):
            response = requests.post(AUTH_REGISTER, json=payload)

        with allure.step("Проверить код ответа 403"):
            assert response.status_code == 403
            assert response.json()["message"] == "Email, password and name are required fields"

        # В этом тесте пользователь не создаётся, поэтому удалять нечего