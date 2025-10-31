import os
import stat
from datetime import datetime

import src.config.functions
import src.config.logger


def output(flags: set, path: str) -> None:
    """
    Выводит имена файлов в директории.

    Args:
        path: Путь к директории.

    Prints:
        Печатает имена файлов.
    """
    pointer = False
    if 'a' in flags or 'all' in flags:
        pointer = True
    if os.listdir(path):
        for file in os.listdir(path):
            if (not file.startswith('.')) or (
                file.startswith('.') and pointer
            ):
                print(file, end=' ')
        print()


def detailed_output(flags: set, path: str) -> None:
    """
    Выводит подробную информацию о файлах в директории.

    Формат вывода: Имя Размер Время_изменения Права_доступа.

    Args:
        path: Путь к директории.

    Prints:
        Печатает подробную информацию о файлах.
    """
    pointer = False
    if 'a' in flags or 'all' in flags:
        pointer = True
    for file in sorted(os.listdir(path)):
        if (not file.startswith('.')) or (file.startswith('.') and pointer):
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
            - 'a'/'all': вывод скрытых файлов.
        paths: Список путей к директориям. Если пустой, то используется текущая

    Prints:
        Печатает содержимое директорий.

    Raises:
        IncorrectFlag: Если указан неверный флаг.
        IsNotDirectory: Если путь не является директорией.
        PathError: Если указана несуществующая директория.
    """
    src.config.functions.is_correct_flag(flags, {'l', 'a', 'all'})
    paths = paths if paths else [os.getcwd()]
    pointer = True if len(paths) > 1 else False
    for path in paths:
        path = src.config.functions.normalize_path(path)
        src.config.functions.is_correct_directory(path)
        try:
            if pointer:
                print(f'{path.split(os.sep)[-1]}: ')
            if 'l' in flags:
                detailed_output(flags, path)
            else:
                output(flags, path)
        except PermissionError:
            print(f'Нет прав на чтение {path}')
            src.config.logger.main_logger.error(f'Нет прав на чтение {path}')
