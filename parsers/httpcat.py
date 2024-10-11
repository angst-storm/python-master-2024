import random
import requests

http_codes = [
    100, 101, 200, 201, 202, 203, 204, 205, 206, 300, 301, 302, 303, 304, 305, 307, 400,
    401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417,
    500, 501, 502, 503, 504, 505
]

def parse() -> dict[str, bytearray]: 
    status_code = random.choice(http_codes)

    response = requests.get(f'https://http.cat/{status_code}')

    return {"result.jpg": response.content}