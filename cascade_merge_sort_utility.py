"""
Модуль Cascade Merge Sort Utility

Этот модуль предоставляет утилиту командной строки для сортировки файлов с использованием алгоритма сортировки слиянием
из модуля `cascade_merge_sort`. Он обрабатывает аргументы командной строки и вызывает функцию `my_sort`
для выполнения сортировки.

Основные функции:
- `main()`: Обрабатывает аргументы командной строки и вызывает функцию `my_sort` для выполнения сортировки.

Пример использования:
```bash
python cascade_merge_sort_utility.py 4.csv -o 5.csv -r -k x -t i
"""
import argparse

from cascade_merge_sort import my_sort


def main() -> None:
    parser = argparse.ArgumentParser(description="Cascade Merge Sort")
    parser.add_argument("src", help="Source file to sort")
    parser.add_argument("-o", "--output", help="Output file (default is to sort in place)")
    parser.add_argument("-r", "--reverse", action="store_true", help="Sort in descending order")
    parser.add_argument("-k", "--key", help="Specify a key function for sorting")
    parser.add_argument("-t", "--type_data", default='i', help="Specify type of data to sort")

    args = parser.parse_args()

    my_sort(args.src, args.output, args.reverse, args.key, args.type_data)


if __name__ == "__main__":
    main()
