"""
Скрипт читает имя аккаунта и роль, создаёт его и назначает заданную роль, 
получает ключи и сохраняет их в `.env` с именами `{name}_key_id` и 
`{name}_secret`.

Для работы необходимы ключи и секрет пользователя с достаточными правами в 
файле `.env` под ключами  `p_key_id` и `p_secret`.

Examples:
    python3 create_service_account.py 's3-admin' 's3e.admin'
"""

import utils
from create_service_account.argparse import parse_args

# Загрузка облачных айди, кредов, токенов
project_id = utils.get_project_id()
token = utils.get_or_refresh_token()
args = parse_args()
acc_name = args.acc_name
acc_role = args.acc_role
utils.check_vars([project_id, token])

# Формирование запроса для создания аккаунта
print("Creating account")
url = "https://iam.api.cloud.ru/api/v1/service-accounts"
headers = utils.post_headers(token)
data = {
    "name": acc_name,
    "description": "",
    "projectId": project_id,
}
# Запрос, сохранение ответа и работа с ошибками
response = utils.post_request(url, headers, data).json()
utils.log_response(acc_name, response)
acc_id = response["service_account"]["id"]
utils.set_env(f"{acc_name}_id", acc_id)
print("Done")

# Назначаем роль
print("Assigning role")
url = "https://iam.api.cloud.ru/api/v1/permissions"
data = {
    "role": acc_role,
    "objectId": project_id,
    "objectType": "resource",
    "subjectId": acc_id,
    "subjectType": "service_account",
    "expiresAt": "2027-09-09T20:45:13.171742Z",
}
utils.post_request(url, headers, data)
print("Done")

# Получаем ключи
print("Issueing keys")
url = "https://iam.api.cloud.ru/api/v1/service-accounts/credentials/access-keys"
data = {
    "serviceAccountId": acc_id,
    "description": "",
    "ttl": "8760h",
}
response = utils.post_request(url, headers, data).json()
utils.set_env(f"{acc_name}_key_id", response["key_id"])
utils.set_env(f"{acc_name}_secret", response["secret"])
print("Done")

print("All done!")
