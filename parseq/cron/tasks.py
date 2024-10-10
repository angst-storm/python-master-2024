import os
import uuid
import dramatiq
import importlib
import importlib.util
import traceback
from django.conf import settings
from django_apscheduler import util

@util.close_old_connections
def send_run_actor(id, name, path):
    run_actor.send(str(uuid.uuid4()), id, name, path)

def import_module_from_path(path):
    spec = importlib.util.spec_from_file_location("module_name", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def prepare_output_dir(run_id):
    result_dir = os.path.join(settings.MEDIA_ROOT, run_id)
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    return result_dir

def save_outputs(dir, files):
    for filename, content in files.items():
        result_path = os.path.join(dir, filename)
        with open(result_path, 'wb') as f:
            f.write(content)

@dramatiq.actor
def run_actor(run_id, parser_id, parser_name, path):
    output_dir = prepare_output_dir(run_id)
    
    print(f"Run parser {parser_name} (ID: {parser_id}) by {path} to {output_dir}...")

    try:
        parser = import_module_from_path(path)
        results = parser.parse()
        save_outputs(output_dir, results)
        print(f'{run_id} Done')
    except Exception:
        print(f'{run_id} Failed')
        errors = {"error.txt": str.encode(traceback.format_exc())}
        save_outputs(output_dir, errors)
        raise
