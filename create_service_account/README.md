# argparse
Для создания индивидуального парсера добавьте его импорт в файл `__init.py__`. Пример:
```python
import argparse
# Настраиваем парсер
def parse_args():
...
```
добавляем в файл `__init.py__`:
```python
from .argparse import parse_args
```
В основном скрипте такой парсер можно подключить по имени скрипта и названию модуля парсера через точку:
```python
from create_service_account.argparse import parse_args
