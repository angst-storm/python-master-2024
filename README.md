# Parseq. Приложение для запуска и оркестрации веб-парсеров

<p align="center">
    <img src="images/banner.png" alt="logo">
</p>

Приложение, содержащее логику управления веб-парсерами (автоматический запуск по расписанию, ручной запуск).

**Основные технологии: [Django](https://github.com/django/django), [Dramatiq](https://github.com/Bogdanp/dramatiq).**

### Требования

1. Пользователь может написать в *файле проекта* скрипт парсера. Через веб-интерфейс он может поставить его на расписание, выключить автоматический запуск и запустить вручную.
2. Каждый парсер имеет название, описание и путь до скрипта, который необходимо выполнить.
3. Пользователь может посмотреть данные по запускам парсеров (время, статус - выполнен, ожидание, ошибка).
4. Несколько простых парсеров (минимум 2) для демонстрации работы приложения. Это может быть парсер погоды, курса валют и т.п.
5. Минимум 2 теста.
6. Для запуска парсеров используется Dramatiq.
7. Возможность выгружать файлы-результаты работы парсеров с помощью REST API.
8. Оформление по [PEP8](https://peps.python.org/pep-0008/).
9. Документация в `README.md` c описанием, стэком, инструкцией по запуску приложения и тестов.

### Стэк

- Python
- Django
- Dramatiq + django_dramatiq
- APScheduler
- UnitTest
- RabbitMQ
- PostgreSQL
- Docker

### Описание

Приложение управляется с помощью панели администратора Django. Для авторизации по умолчанию используется username `admin` и пароль `admin`.

В панели зарегистрированы классы `Parser` и `Task`. `Parser` содержит обязательное поле `name`, текстовое поле `description`, обязательный файл `script`, поля для конфигурации автоматического запуска (`scheduled_time`, `repeat_after`). Пользователь может создавать объекты класса `Parser` и настраивать их. `Task` содержит `run_id` в формате UUID, `status` (enum - `enqueued`, `running`, `completed`, `error`), `created_time`, `updated_time` и ссылку на объект `Parser`. `Task` реализован в библиотеке [django_dramatiq](https://github.com/Bogdanp/django_dramatiq).

Скрипты парсеров пишутся на языке Python в файле с форматом `.py`. Скрипт может импортировать только библиотеки, которые были заранее установлены для приложения (см. `requirements.txt`). Скрипт должен реализовывать функцию `parse`, которая не принимает аргументов и возвращает словарь с файлами-результатами в формате `{'filename': b'content'}`. После завершения скрипта файлы-результаты можно получить по ссылке `<url>/<run_id>/<filename>`. Например: `http://localhost:8000/69bff530-1437-4891-b35c-1d5242057b40/result.jpg`. В случае, если парсер завершается с ошибкой, текст ошибки можно получить в панели администратора и по ссылке `<url>/<run_id>/error.txt`.

После активации ручного запуска в панели администратора парсер ставится в очередь RabbitMQ и запускается с помощью Dramatiq. После настройки автоматического запуска, планированием запуска занимается [APScheduler](https://apscheduler.readthedocs.io/en/3.x/) ([рекомендумая библиотека](https://dramatiq.io/cookbook.html#scheduling) для Dramatiq). По достижению необходимого времени, планировщик передает данные для запуска в Dramatiq.

Реализованы два парсера - парсер, получающий случайную картинку кота, соответствующую коду HTTP (`parsers/httpcat.py`) и парсер, представляющий в человекочитаемом виде информацию о войнах в игре Eve Online, объявленных за последние 24 часа (`parsers/evewars.py`). Для демонстрации возможностей обработки ошибок, так же реализован парсер `parsers/error.py`, выбрасывающий исключение при запуске.

Реализованы два теста - тест парсера `evewars.py` с использованием [UnitTest](https://docs.python.org/3/library/unittest.html) (см. `parsers/test.py`) и тест ручного запуска парсеров в Django Admin с использованием UnitTest и `django.test` (см. `parseq/cron/tests.py`).

База данных [PostgreSQL](https://www.postgresql.org/) и брокер [RabbitMQ](https://www.rabbitmq.com/) разворачиваются в [Docker](https://www.docker.com/) с помощью docker-compose.

### Использование

#### Запуск

Подготовка:
- Установите Docker
- Настройте окружение Python

```shell
docker compose -f deploy/docker-compose.yaml up -d
pip install -r requirements.txt
cd parseq
python manage.py migrate
python manage.py createsuperuser --no-input # По умолчанию - admin:admin
python manage.py runserver --noreload
# Запустите в другом процессе
python manage.py rundramatiq
```

#### Тесты

```shell
(cd parsers && python -m unittest)
(cd parseq && python manage.py test)
```

#### Makefile

Многие команды реализованы в `Makefile`. Для их использования установите [Make](https://www.gnu.org/software/make/).

```shell
make deploy
make init
make test
make runserver
make rundramatiq
make destroy
make clear -i
```
