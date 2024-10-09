import random
import requests

def parse() -> dict[str, str]: 
    status_code = random.randint(100, 500)

    response = requests.get(f'https://http.cat/{status_code}')

    return {"result.jpg": response.content}