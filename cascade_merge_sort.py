"""
Модуль Cascade Merge Sort

Модуль cascade_merge_sort предоставляет функционал для сортировки файлов в форматах .txt и .csv
с использованием каскадной сортировки.

Основные функции:
- my_sort(src, output, reverse, key, type_data): Сортирует файл в формате .txt или .csv, используя каскадную сортировку.
"""
import csv
import os
import pathlib
import shutil
import tempfile
from typing import Union, Optional, Callable

from cascade_maerge_sort_csv import write_sorted_chunk, merge_temp_files
from cascade_maerge_sort_txt import write_sorted_chunk_txt, merge_temp_files_txt

PathType = Union[str, pathlib.Path]


def my_sort(src: PathType, output: Optional[PathType] = None, reverse: bool = False,
            key: Optional[Callable] = None, type_data: str = 'i') -> None:
    """
    Сортирует файл в формате .txt или .csv, используя каскадную сортировку.

    :param src: Путь к файлу для сортировки. Может быть строкой с путем к одному файлу или списком путей.
    :param output: Путь к выходному файлу. Если не указан, перезаписывает исходный файл.
    :param reverse: Если True, выполняет сортировку в обратном порядке.
    :param key: Функция, используемая для извлечения ключа сравнения.
    :param type_data: Тип данных, 'i' для целых чисел, 'f' для чисел с плавающей точкой, 's' для строк.
    :return: None
    """
    if isinstance(src, str):
        src = [src]

    if isinstance(src, list):
        for src in src:
            src = pathlib.Path(src)

            if output is not None and isinstance(output, str):
                output = pathlib.Path(output)

            if output is None:
                output = src

            if os.path.exists(src):
                file_extension = src.suffix.lower()
                out_file_extension = output.suffix.lower()

                if file_extension in ['.txt', '.csv']:
                    temp_dir = pathlib.Path(tempfile.mkdtemp(suffix='_temp', prefix="a", dir='.'))
                    chunk_files = []
                    with open(src, 'r', newline='') as src_file:
                        reader = csv.reader(src_file)
                        if file_extension == '.csv':

                            if not key:
                                raise ValueError("Key is not defined")

                            if out_file_extension != '.csv':
                                raise ValueError("Wrong output format")

                            title = next(reader)

                            if len(title) == 1:
                                title = title[0].split(',')

                            if isinstance(key, str):
                                if key in title:
                                    key = title.index(key)
                                    chunk = []
                                    size = 0
                                    max_lines = 3

                                    for row in reader:
                                        if size >= max_lines:
                                            chunk_file = temp_dir.joinpath(f'chunk_{len(chunk_files)}.csv')
                                            write_sorted_chunk(chunk, chunk_file, key, title, type_data, reverse)
                                            chunk_files.append(chunk_file)
                                            chunk = []
                                            size = 0
                                        chunk.append(row)
                                        size += 1

                                    if chunk:
                                        chunk_file = temp_dir.joinpath(f'chunk_{len(chunk_files)}.csv')
                                        write_sorted_chunk(chunk, chunk_file, key, title, type_data, reverse)
                                        chunk_files.append(chunk_file)

                                    merge_temp_files(chunk_files, output, key, title, type_data, reverse)
                                    shutil.rmtree(temp_dir)

                                else:
                                    raise ValueError(f"Collumn with name {key} not found")

                            else:
                                raise ValueError("Key is not string format")

                        if file_extension == '.txt':
                            if out_file_extension != '.txt':
                                raise ValueError("Wrong output format")

                            chunk = []
                            size = 0
                            max_lines = 3

                            for row in reader:
                                if size >= max_lines:
                                    chunk_file = temp_dir.joinpath(f'chunk_{len(chunk_files)}.txt')
                                    write_sorted_chunk_txt(chunk, chunk_file, type_data, reverse)
                                    chunk_files.append(chunk_file)
                                    chunk = []
                                    size = 0
                                chunk.append(row)
                                size += 1

                            if chunk:
                                chunk_file = temp_dir.joinpath(f'chunk_{len(chunk_files)}.txt')
                                write_sorted_chunk_txt(chunk, chunk_file, type_data, reverse)
                                chunk_files.append(chunk_file)

                            merge_temp_files_txt(chunk_files, output, type_data, reverse)
                            shutil.rmtree(temp_dir)

                else:
                    raise ValueError("File extension is not supported")

            else:
                raise ValueError(f'File {src} was not found')
