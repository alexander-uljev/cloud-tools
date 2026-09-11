import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Скрипт для создания сервисного аккаунта, присвоения роли и выпуска ключей."
    )

    parser.add_argument(
        "acc_name",
        help="Имя аккаунта без пробелов",
    )

    parser.add_argument(
        "acc_role",
        help="Роль в формате строки через точку. Например s3e.admin",
    )

    parser.add_argument("-v", "--verbose", help="Подробный вывод")
    return parser.parse_args()
