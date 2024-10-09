import random
import requests
from PIL import Image
import uuid
import os

status_code = random.randint(100, 500)

run_id = uuid.uuid4()
result_path = f'media/{run_id}/result.jpg'

response = requests.get(f'https://http.cat/{status_code}')

directory = os.path.dirname(result_path)
if not os.path.exists(directory):
    os.makedirs(directory)
with open(result_path, 'wb') as f:
    f.write(response.content)