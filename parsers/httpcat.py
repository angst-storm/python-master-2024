import random
import requests
from PIL import Image

status_code = random.randint(100, 500)

response = requests.get(f'https://http.cat/{status_code}', stream=True)
image = Image.open(response.raw)
image.show()