import os
import uuid
import dramatiq
import importlib
import importlib.util
from django.conf import settings
from django_apscheduler import util

@util.close_old_connections
def send_run_actor(name, path):
    run_actor.send(str(uuid.uuid4()), name, path)

def import_module_from_path(path):
    spec = importlib.util.spec_from_file_location("module_name", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

@dramatiq.actor
def run_actor(run_id, name, path):
    result_dir = os.path.join(settings.MEDIA_ROOT, run_id)
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    print(f"Run parser {name} by {path} to {result_dir}")

    parser = import_module_from_path(path)

    results = parser.parse()

    for filename, content in results.items():
        result_path = os.path.join(result_dir, filename)
        with open(result_path, 'wb') as f:
            f.write(content)