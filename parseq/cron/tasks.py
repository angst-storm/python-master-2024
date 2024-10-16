import importlib
import importlib.util
import os
import traceback
import uuid

import dramatiq
from django.conf import settings

from .models import Parser


def send_run_actor(parser_id):
    """Создает Run ID и отправляет актор в Dramatiq"""
    run_actor.send(str(uuid.uuid4()), parser_id)


def import_module_from_path(path):
    """Импортирует скрипт из файла по заданному пути"""
    spec = importlib.util.spec_from_file_location("module_name", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare_output_dir(run_id):
    """Создает директорию для хранения результатов работы парсера"""
    output_dir = os.path.join(settings.MEDIA_ROOT, run_id)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def save_outputs(output_dir, files):
    """
    Сохраняет результаты работы парсера в выбранную директорию

    Args:
        output_dir (str): Путь до папки, где необходимо сохранить данные
        files (dict[str, bytearray]): Словарь с именами файлов -> содержимым
        в формате массива байтов
    """
    for filename, content in files.items():
        result_path = os.path.join(output_dir, filename)
        with open(result_path, "wb") as f:
            f.write(content)


@dramatiq.actor
def run_actor(run_id, parser_id):
    """Актор Dramatiq, запускающий скрипт парсера с ID parser_id
    и сохраняющий результаты работы или ошибку"""
    output_dir = prepare_output_dir(run_id)

    parser = Parser.objects.get(id=parser_id)
    path = parser.script.path

    print(f"Run parser {parser.name} (ID: {parser_id}) by {path} to {output_dir}...")

    try:
        parser = import_module_from_path(path)
        results = parser.parse()
        save_outputs(output_dir, results)
        print(f"{run_id} Done")
    except:
        print(f"{run_id} Failed")
        errors = {"error.txt": str.encode(traceback.format_exc())}
        save_outputs(output_dir, errors)
        raise
