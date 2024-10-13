import importlib
import importlib.util
import io
import sys

from PIL import Image, UnidentifiedImageError


def import_module_from_path(path):
    spec = importlib.util.spec_from_file_location("module_name", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pretty_print(outputs):
    for filename, content in outputs.items():
        print(f"\n{filename}:\n")

        try:
            print(content.decode())
            return
        except UnicodeDecodeError:
            pass

        try:
            image = Image.open(io.BytesIO(content))
            image.show()
            print("*showed*")
        except UnidentifiedImageError:
            print(content)


if __name__ == "__main__":
    path = sys.argv[1]
    module = import_module_from_path(path)
    outputs = module.parse()
    pretty_print(outputs)
