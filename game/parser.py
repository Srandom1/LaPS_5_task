from file_manager import open_file
from word.field import Field
from models import models


def generate_field_from_string(source: str, size = 20) -> Field:
    cleared_source = delete_line_break(source)
    print(cleared_source)
    elements = separate_elements_by_comma(cleared_source)


def delete_line_break(source: str):
    striped = source.replace("\n", "")
    return striped


def separate_elements_by_comma(source: str) -> list[str]:
    elements = list()
    part_start_index = 0

    for index in range(len(source)):
        if source[index] != ",":
            continue
        elements.append(source[part_start_index:index])
        part_start_index = index

    if part_start_index != len(source) - 1:
        elements.append(source[:part_start_index])

    return elements


def add_field_element(field:Field)


if __name__ == "__main__":
    source = open_file("level1.txt")
    generate_field_from_string(source)
