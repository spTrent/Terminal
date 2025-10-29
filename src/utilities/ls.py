import os
import stat
from datetime import datetime

import src.config.functions


def output(path: str) -> None:
    """
    Выводит имена файлов в директории, игнорируя скрытые.

    Args:
        path: Путь к директории.

    Prints:
        Печатает имена файлов.
    """
    for file in os.listdir(path):
        if not file.startswith('.'):
            print(file, end=' ')
    print()


def detailed_output(path: str) -> None:
    """
    Выводит подробную информацию о файлах в директории.

    Формат вывода: Имя Размер Время_изменения Права_доступа.

    Args:
        path: Путь к директории.

    Prints:
        Печатает подробную информацию о файлах.
    """
    for file in sorted(os.listdir(path)):
        if not file.startswith('.'):
            file_path = os.path.join(path, file)
            file_stat = os.stat(file_path)
            modes = stat.filemode(file_stat.st_mode)
            size = file_stat.st_size
            time_mode = datetime.fromtimestamp(int(file_stat.st_mtime))
            time_mode_f = time_mode.strftime('%b %d %H:%M')
            print(f'{file:15} {size:7} {time_mode_f:12} {modes:10}')


def ls(flags: set, paths: list[str]) -> None:
    """
    Выводит содержимое директорий, указанных в paths.

    Args:
        flags: множество флагов:
            - 'l': подробный вывод.
        paths: Список путей к директориям. Если пустой, то используется текущая

    Prints:
        Печатает содержимое директорий.

    Raises:
        IncorrectFlag: Если указан неверный флаг.
        IsNotDirectory: Если путь не является директорией.
        PathError: Если указана несуществующая директория.
    """
    src.config.functions.is_correct_flag(flags, {'l'})
    paths = paths if paths else [os.getcwd()]
    for path in paths:
        path = src.config.functions.normalize_path(path)
        src.config.functions.is_correct_directory(path)
        print(f'{path.split(os.sep)[-1]}: ')
        if flags:
            detailed_output(path)
        else:
            output(path)
        print()
