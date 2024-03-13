"""
Модуль Cascade Merge Sort TXT

Этот модуль содержит функции для сортировки текстовых файлов с использованием алгоритма сортировки слиянием.
Он предоставляет функции для преобразования типов данных, записи отсортированных блоков данных в файл
и объединения временных файлов в один.

Основные функции:
- data_type(row, data_type_key): Преобразует строку в нужный формат данных для сортировки.
- write_sorted_chunk_txt(data_chunk, file, data_type_key, reverse): Записывает отсортированный блок данных в файл.
- merge_temp_files_txt(data_chunk, output_file, data_type_key, reverse): Объединяет все временные файлы в один.
"""
import csv
from typing import List, Union


def data_type(row: str, data_type_key: str) -> Union[int, float, str]:
    """
    Преобразует строку в нужный формат данных для сортировки.

    :param row: Строка для преобразования.
    :param data_type_key: Ключ типа данных для преобразования ('i' для int, 'f' для float, 's' для str).
    :return: Преобразованная строка.
    :raises ValueError: Если data_type_key не 'i', 'f' или 's'.
    """
    match data_type_key:
        case 'i':
            return int(row)

        case 'f':
            return float(row)

        case 's':
            return str(row)

        case _:
            raise ValueError("Wrong type. Only str or int or float")


def write_sorted_chunk_txt(data_chunk: List[str], file: str, data_type_key: str, reverse: bool) -> None:
    """
    Записывает отсортированный блок данных в файл.

    :param data_chunk: Блок данных для сортировки.
    :param file: Путь к файлу для записи.
    :param data_type_key: Ключ типа данных для сортировки.
    :param reverse: Если True, сортирует в обратном порядке.
    :return: None
    """
    with open(file, 'w', newline='') as temp_file:
        csv_writer = csv.writer(temp_file)
        for row in sorted(data_chunk[0:], key=lambda rows: data_type(rows[0], data_type_key), reverse=reverse):
            csv_writer.writerow(row)


def merge_temp_files_txt(data_chunk: List[str], output_file: str, data_type_key: str, reverse: bool) -> None:
    """
    Объединяет все временные файлы в один.

    :param data_chunk: Список путей к временным файлам.
    :param output_file: Путь к выходному файлу.
    :param data_type_key: Ключ типа данных для сортировки.
    :param reverse: Если True, сортирует в обратном порядке.
    :return: None
    """
    if len(data_chunk) <= 1:
        return

    end_of_file_flag = '♥'
    file_row_index_dict = {file_num: 0 for file_num in range(len(data_chunk))}
    temp_list = [end_of_file_flag] * len(data_chunk)

    while True:
        file_readers = [csv.reader(open(input_file, 'r', newline='')) for input_file in data_chunk]

        for i, file_reader in enumerate(file_readers):
            file_rows = list(file_reader)
            if temp_list[i] == end_of_file_flag:
                if file_row_index_dict[i] < len(file_rows):
                    temp_list[i] = file_rows[file_row_index_dict[i]]
                    file_row_index_dict[i] += 1

        if all(row == end_of_file_flag for row in temp_list):
            break

        valid_rows = [row for row in temp_list if row != end_of_file_flag]
        min_row = min(valid_rows, key=lambda row: data_type(row[0], data_type_key)) \
            if not reverse else max(valid_rows, key=lambda row: data_type(row[0], data_type_key))
        min_index = temp_list.index(min_row)

        with open(output_file, 'a', newline='') as result_file:
            writer = csv.writer(result_file)
            writer.writerow(min_row)

        temp_list[min_index] = end_of_file_flag
