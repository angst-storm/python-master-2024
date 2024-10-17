"""Парсер, получающий случайный мем с котом.

Выбирает псевдослучайный валидный код HTTP ответа
и получает изображение соответствующее этому коду с ресурса https://http.cat/.
"""

import random
from itertools import chain

import requests

http_codes = list(
    chain(
        range(100, 102),
        range(200, 207),
        range(300, 308),
        range(400, 418),
        range(500, 506),
    )
)

TIMEOUT_SEC = 60


def parse() -> dict[str, bytearray]:
    """Функция парсинга.

    Получает случайный код HTTP и запрашивает изображение.
    """
    status_code = random.choice(http_codes)  # noqa: S311 not important

    response = requests.get(f"https://http.cat/{status_code}", timeout=TIMEOUT_SEC)

    return {"result.jpg": response.content}
