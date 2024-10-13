import random

import requests

http_codes = (
    range(100, 102) + range(200, 207) + range(300, 308) + range(400, 418) + (500, 506)
)


def parse() -> dict[str, bytearray]:
    status_code = random.choice(http_codes)

    response = requests.get(f"https://http.cat/{status_code}")

    return {"result.jpg": response.content}
