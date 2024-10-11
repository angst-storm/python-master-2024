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
- APScheduler + django_apscheduler
- UnitTest
- RabbitMQ
- PostgreSQL
- Docker
- Yandex Cloud

### Описание

Приложение, база данных [PostgreSQL](https://www.postgresql.org/), брокер [RabbitMQ](https://www.rabbitmq.com/), развернуты в [Docker](https://www.docker.com/) на виртуальной машине на [Yandex Cloud](https://yandex.cloud/ru/). Доступно по адресу [https://parseq.sergei-kiprin.ru](https://parseq.sergei-kiprin.ru). Для хранения скриптов и файлов используется S3 Object Storage.

Приложение управляется с помощью панели администратора Django. В ней зарегистрированы классы `Parser` и `Task`. `Parser` содержит обязательное поле `name`, текстовое поле `description`, обязательный файл `script`, поля для конфигурации автоматического запуска (`scheduled_time`, `repeat_after`). Пользователь может создавать объекты класса `Parser` и настраивать их. `Task` содержит `run_id` в формате UUID, `status` (enum - `enqueued`, `running`, `completed`, `error`), `created_time`, `updated_time` и ссылку на объект `Parser`.

Скрипты парсеров пишутся на языке Python в файле с форматом `.py`. Скрипт может импортировать только библиотеки, которые были заранее установлены для приложения (см. requirements.txt). Скрипт должен реализовавать функцию `parse`, которая не принимает аргументов и возвращает словарь с файлами-результатами в формате `{'filename': bytes(file_content)}`. После завершения скрипта файлы-результаты можно получить по ссылке `<url>/<run_id>/<filename>`. Например: `http://localhost:8000/69bff530-1437-4891-b35c-1d5242057b40/result.png`. В случае, если парсер завершается с ошибкой, текст ошибки можно получить в панели администратора и по ссылке `<url>/<run_id>/error.txt`.

После активации ручного запуска в панели администратора парсер ставится в очередь RabbitMQ и запускается с помощью Dramatiq. После настройки автоматического запуска, планированием запуска занимается [APScheduler](https://apscheduler.readthedocs.io/en/3.x/) ([рекомендумая библиотека](https://dramatiq.io/cookbook.html#scheduling) для Dramatiq). По достижению необходимого времени, Scheduler передает данные для запуска в Dramatiq. Лучше выбирать время для запуска как минимум через три минуты от текущего момента, так как APScheduler не запускает задачи немедленно.

Реализованы два парсера - парсер, получающий случайную картинку кота, соответствующую коду HTTP (https://http.cat/) и парсер, представляющий в человекочитаемом виде информацию о войнах в игре Eve Online, объявленных за последние 24 часа.

Для тестирования используются возможности `django.test` и библиотека [UnitTest](https://docs.python.org/3/library/unittest.html).

### Инструкция по запуску

```shell
docker compose -f deploy/docker-compose.yaml up -d
# setup python env
pip install -r requirements.txt
cd parseq
python manage.py migrate
python manage.py createsuperuser --no-input # default - admin:admin
python manage.py runserver
# run next in parallel
python manage.py rundramatiq
```

### Задачи

- Режим DEBUG=False
- Изменение аргументов Job при изменении модели
- Написать два теста
- Проблемы с конкуренцией за подключение к БД
https://stackoverflow.com/questions/53578752/updating-django-models-with-multiprocessing-pool-locks-up-database
https://stackoverflow.com/questions/8242837/django-multiprocessing-and-database-connections/10684672#10684672
- *Развернуть в Yandex Cloud + S3
