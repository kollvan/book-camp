# BookCamp
---
Bookcamp - это сайт являющийся онлайн библиотекарем. Платформа используется для поиска, систематизации и отслеживания различной литературы.
![Inventory](https://github.com/user-attachments/assets/bb2baae5-2f49-4802-80cc-7cc54d799f85)

## Содержание
---
- [[#Технологии]]
- [[#Использование]]
- [[#Настройка окружения]]
- [[#Тестирование]]
- [[#ToDo]]

## Технологии
---
- [python](https://docs.python.org/3/)
- [selenium](https://selenium-python.readthedocs.io/)
- [postgresql](https://www.postgresql.org/docs/)
- [redis](https://redis.io/docs/latest/)
- [django](https://docs.djangoproject.com/en/5.2/)
- [drf](https://www.django-rest-framework.org/)
- [docker](https://www.docker.com/)
- [nginx](https://nginx.org/)

## Использование
---
Для работы приложения необходимо настроить окружение (подробнее см. [[#Настройка окружения]]).

Отдельный запуск приложения.
```shell
python ./bookcamp/manage.py runserver
```

Запуск в docker.
```shell
docker compose -f ./book-camp/compose.yml up
```

## Настройка окружения
---
Для запуске приложения необходим файл `.env` содержащий переменные среды.
Создание файла:
```shell
touch ./book-camp/.env
```

### Список используемых переменных

| Переменная                | Описание                                                                                                                                                                                                                                        | Обязательная     | Пример                    |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | ------------------------- |
| DJANGO_KEY                | Секретный ключ, используемый для криптографический операций [django secret_key](https://docs.djangoproject.com/en/6.0/ref/settings/#std-setting-SECRET_KEY) Генерируется с помощью функции `django.core.management.utils.get_random_secret_key` | Да               | -                         |
| DJANGO_ALLOWED_HOSTS      | Список хостов/доменов которые может обслуживать приложение. [django allowed hosts](https://docs.djangoproject.com/en/6.0/ref/settings/#allowed-hosts)                                                                                           | Да (DEBUG=False) | 127.0.0.1 localhost [::1] |
| DJANGO_DEBUG              | Режим запуска приложения [django debug](https://docs.djangoproject.com/en/6.0/ref/settings/#debug) Если переменная не задана, то приложение запускается в режиме debug.                                                                         | Нет              | True/False                |
| POSTGRES_HOST             | Хост на котором расположен СУБД postgresql. При запуске через docker compose должна принимать значение psdb.                                                                                                                                    | Да               | psdb                      |
| POSTGRES_PORT             | Порт для доступа к субд postgresql                                                                                                                                                                                                              | Да               | 5432                      |
| POSTGRES_DB_NAME          | Имя создаваемой базы данных в postgresql.                                                                                                                                                                                                       | Да               | bookcamp                  |
| POSTGRES_USER             | Имя пользователя базы данных в postgresql.                                                                                                                                                                                                      | Да               | bookman                   |
| POSTGRES_PASS             | Пароль пользователя базы данных в postgresql.                                                                                                                                                                                                   | Да               | -                         |
| REDIS_USERNAME            | Имя пользователя для доступа к redis.                                                                                                                                                                                                           | Нет              | bookman                   |
| REDIS_PASSWORD            | Пароль пользователя по умолчания для доступа к redis. Можно использовать вместо REDIS_USERNAME и REDIS_USER_PASSWORD.                                                                                                                           | Нет              | -                         |
| REDIS_HOST                | Хост на котором расположен redis. При запуске через docker compose должна принимать значение rcache.                                                                                                                                            | Да (DEBUG=False) | rcache                    |
| REDIS_USER_PASSWORD       | Пароль пользователя REDIS_USERNAME для доступа к redis.                                                                                                                                                                                         | Нет              | -                         |
| REDIS_PORT                | Порт на котором  расположен redis.                                                                                                                                                                                                              | Да (DEBUG=False) | 6069                      |
| EMAIL_HOST                | Хост для отправки писем. [django email host](https://docs.djangoproject.com/en/6.0/ref/settings/#email-host)                                                                                                                                    | Да (DEBUG=False) | 'smtp.gmail.com'          |
| EMAIL_HOST_PASSWORD       | Пароль для доступа к серверу на EMAIL_HOST. [django email password](https://docs.djangoproject.com/en/6.0/ref/settings/#email-host-password)                                                                                                    | Да (DEBUG=False) | -                         |
| EMAIL_HOST_USER           | Пользователь используемый для отправки писем. [djangoe email user](https://docs.djangoproject.com/en/6.0/ref/settings/#email-host-user)                                                                                                         | Да (DEBUG=False) | bookcamp8@gmail.com       |
| DJANGO_SUPERUSER_USERNAME | Содержит имя супер пользователя приложения.                                                                                                                                                                                                     | Нет              | bookman                   |
| DJANGO_SUPERUSER_PASSWORD | Содержит пароль супер пользователя приложения.                                                                                                                                                                                                  | Нет              | -                         |
| DJANGO_SUPERUSER_EMAIL    | Содержит почту супер пользователя приложения.                                                                                                                                                                                                   | Нет              | bookcamp8@gmail.com       |

## Тестирование
---
Для тестирования используется пакет selenium.

Для запуска тестов необходимо воспользоваться:

```bash
docker exec backend-bookcamp python manage.py test
```

Для запуска функциональных тестов необходимо воспользоваться:

```bash
docker exec backend-bookcamp python manage.py test .\functional_tests\
```