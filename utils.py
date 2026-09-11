"""
Сборник полезных функций для формирования запросов к REST API, работы с ключами,
токенами и дебагу проблем с вызовами.
"""

import json
import os
import sys

import dotenv
import requests
from requests.exceptions import HTTPError

from exceptions import TokenExpiredError


def get_request(url, headers):
    response = requests.get(url, headers=headers)
    check_status(response)
    return response


def post_request(url, headers, data):
    response = requests.post(url, headers=headers, json=data)
    check_status(response)
    return response


def check_status(response):
    """ Место для обработки ошибок вызовов в API и управления выполнением скрипта на их основе
    Args:
        response: requests.Response
    Raises:
        HTTPError - перевыбрасывает исключение с более простым сообщением
        TokenExpiredError - для обработки и получения нового
    """
    try:
        response.raise_for_status()
    except HTTPError as err:
        if response.status_code == 401: # Не авторизован - токен просрочен
            raise TokenExpiredError("Your token expired. Please request a new one")
        if response.status_code == 400: # Неправильный метод вызова, неправильный формат данных, неверные ключи
            raise HTTPError(
                f"Bad request:\n{err}\nThe response was {response.text}"
            ) from err
        if response.status_code == 404: # Ресурс не найден, выходим
            exit(f"Resourse not found\n{err}\n{response.text}")
        raise HTTPError(
            f"Request failed:\n{err}\nThe response was {response.text}"
        ) from err


def log_response(name, content):
    """ Сохраняет ответ как есть, добавляя его в конец файла с именем $name.json """
    try:
        with open(f"{name}.json", "a", encoding="utf-8") as file:
            file.write(json.dumps(content, indent=4))
    except OSError as error:
        print(f"Не смог сохранить данные в {name}.json, ошибка: {error}")


def check_vars(vars):
    """ Проверяет список переменных на пустоту (через boolean(x)) и кидает исключение, если хоть одна не была инициализирована """
    if not all(vars):
        raise ValueError(
            "Ошибка: Переменные не инициализированы! Проверьте файл .env и передайте параметры скрипта"
        )

def refresh_token():
    """ Получает новый IAM-токен и сохраняет его в `.env`. Нужны ключи пользователя с достаточными для этого правами. Тут можно поменять названия ключей на свои, это безопасно, но не забудте отразить изменения в `.env` """
    key_id = get_env("p_key_id")
    key_secret = get_env("p_secret")
    check_vars([key_id, key_secret])

    url = "https://iam.api.cloud.ru/api/v1/auth/token"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "keyId": key_id,
        "secret": key_secret,
    }

    response = post_request(url, headers, data).json()
    set_env("token", response["access_token"])
    return response["access_token"]


def get_or_refresh_token():
    """ Делает пробный запрос с текущим токеном и получает новый, если старый недействителен """
    owner_id = get_env("owner_id")
    org_id = get_env("org_id")
    token = get_token()
    url = f"https://iam.api.cloud.ru/api/v1/customers/{org_id}/users/{owner_id}"
    headers = get_headers(token)
    try:
        get_request(url, headers)
    except TokenExpiredError:
        return refresh_token()
    return token


def get_project_id():
    return get_env("project_id")


def set_env(key, value):
    dotenv.load_dotenv()
    dotenv_path = ".env"
    dotenv.set_key(dotenv_path, key, value)
    return True


def get_env(key):
    dotenv.load_dotenv()
    return os.getenv(key)


def get_token():
    return get_env("token")


def check_argv(n):
    """ Для проверки нужного количества переданных параметров вызова скрипта """
    if len(sys.argv) < n:
        raise ValueError("Не переданы параметры в скрипт, сверьтесь с документацией")


def get_argv(n):
    """ Для простого обращения к параметрам вызова скрипта """
    return sys.argv[n]


def format_response(response):
    return json.dumps(response.json(), indent=4)


def get_header():
    return {
        "accept": "application/json",
    }


def get_headers(token):
    return {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }


def post_headers(token):
    return {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
