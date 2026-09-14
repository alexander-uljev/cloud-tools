# cloud-tools
Пакет для более удобной работы с публичным облачным API. 

## Возможности
- Автоматическая проверка истечения срока действия токенов (JWT).
- Простое формирование запросов
- Автоматическое сохранение ключей и имён аккаунтов
- Более понятная работа с ошибками в ответах от API

## Установка
Скачайте проект и установите зависимости, находясь в его папке.
```bash
pip install -r requirements.txt
```

## Быстрый старт
Создайте файл `.env` в корне проекта и укажите ваши ключи `p_key_id` и `p_secret`

## Использование
В текущей версии основную ценность представляет модуль `utils`, содержащий несколько функций облегчающих формирование запросов и работу с ключами. Пример:
```python
import utils
from create_service_account.argparse import parse_args

# Загрузка облачных айди, кредов, токенов, аргументов
project_id = utils.get_project_id()
token = utils.get_or_refresh_token()
# Тут можно вставить значение вручную, если не хочется передавать их аргументами
args = parse_args()
acc_name = args.acc_name 
acc_role = args.acc_role
utils.check_vars([project_id, token])

# Формирование запроса
url = "https://iam.api.cloud.ru/api/v1/service-accounts"
headers = utils.post_headers(token)
data = {
    "name": acc_name,
    "description": "DO NOT DELETE THIS ACCOUNT!",
    "projectId": project_id,
}
# Запрос, сохранение ответа и работа с ошибками
response = utils.post_request(url, headers, data).json()
utils.log_response(acc_name, response)
acc_id = response["service_account"]["id"]
utils.set_env(f"{acc_name}_id", acc_id)
```

Авторизационные данные хранятся в .env файле. **Это не подходит для прод среды**, но удобно для домашнего использования. **Не публикуйте и не делитесь .env файлами**. 

Скрипты написаны для примера, но могут быть использованы по назначению. `create_service_account.py` позволяет быстро создать сервисный аккаунт, назначить ему права и получить ключи (автоматически сохраняются в `.env`). Пример вызова:
```
python3 create_service_account.py 's3-admin' 's3e.admin'
```

### argparse
Для создания индивидуальных парсеров аргументов скриптов поместите код в папку с именем скрипта и добавьте его импорт в файл `__init.py__` в той же папке. Пример: для скрипта `create_service_account.py` создана папка `create_service_account`, в которой лежит `argparse.py` с кодом:
```python
import argparse
# Настраиваем парсер
...
```
и файл файл `__init.py__`:
```python
from .argparse import parse_args
```
В основном скрипте такой парсер можно подключить по имени скрипта и названию модуля парсера через точку:
```python
from create_service_account.argparse import parse_args
```

## Заключение
Пользуйтесь с осторожностью, берегите своё время, развивайте свои навыки
