import os

def read_file_as_string(file_path):
    """Возвращает прочитанный файл как строку"""
    with open(file_path, "r") as fl:
        return fl.read()

IMAGES_PATH = os.path.join(os.path.dirname(__file__), 'images')
LEVELS_PATH = os.path.join(os.path.dirname(__file__), 'levels')