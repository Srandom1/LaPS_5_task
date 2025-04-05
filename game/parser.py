import re

from file_manager import open_file
from game.models.field import Field
from models import models


def generate_field_from_string(source: str, x_size=20, y_size=20) -> Field:
    game_field = Field(x_size, y_size)
    source_without_spawn, start_cell = extract_start_field(source)


    cleared_source = delete_line_break(source_without_spawn)
    print(cleared_source)
    elements = separate_elements_by_comma(cleared_source)
    for element in elements:
        extracted_cell = parse_field_element(element)
        game_field.change_cell(extracted_cell.x, extracted_cell.y, extracted_cell)

    #На всякий случай в конце, если пользователь криво задаст уровень
    game_field.change_cell(start_cell.x, start_cell.y, start_cell)

def delete_line_break(source: str):
    new_string = source.replace("\n", "")
    return new_string


# Ух тут немного говнокода, но потерпите, ниче страшного
def extract_start_field(source: str) -> tuple:
    """Возвращает кортеж из 2х элементов, первый из которых - строка с вырезанной частью, касающейся описания,
     точки спавна второй поле"""
    splited = source.split(":")
    matches = re.findall(r"\d+", splited[0])
    return splited[1], models.Cell(cell_status=models.CellStatus.ENABLE, y=matches[0], x=matches[1])


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


def parse_field_element(field_source: str) -> models.Cell:
    possible_states = {"enable": models.Cell(cell_status=models.CellStatus.ENABLE),
                       "finish": models.Cell(cell_status=models.CellStatus.FINISH),
                       "disable": models.Cell(cell_status=models.CellStatus.DISABLE),
                       "box": models.Cell(cell_status=models.CellStatus.ENABLE, is_box_inside=True)
                       }
    possible_states: dict[str, models.Cell]

    coordinates = re.findall(r"\d+", field_source)
    for state in possible_states:
        if state in field_source:
            cell_model = possible_states[state]
            cell_model.coordinates = models.Coordinates(int(coordinates[1]), int(coordinates[0]))
            return cell_model
    raise ValueError(f"Can't parse string! Unable to extract cell status. Problem string: {field_source}")


if __name__ == "__main__":
    source = open_file("level1.txt")
    generate_field_from_string(source)
