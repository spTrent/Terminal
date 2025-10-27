import os
import stat
from datetime import datetime

import src.config.functions


def output(path: str) -> None:
    """
    Выводит файлы, расположенные в path, игнорируя скрытые.

    Args:
        path(str) - исходный путь.

    Returns:
        str - имена нескрытых файлов в path.
    """
    for file in os.listdir(path):
        if not file.startswith('.'):
            print(file, end=' ')
    print()


def detailed_output(path: str) -> None:
    """
    Выводит подробную информацию про файлы,
    расположенные в path, игнорируя скрытые.
    В формате: Имя Размер Время изменения Разрешения.

    Args:
        path(str) - исходный путь.

    Returns:
        str - информация про файлы, расположенные в path.
    """
    for file in sorted(os.listdir(path)):
        if not file.startswith('.'):
            file_path = os.path.join(path, file)
            file_stat = os.stat(file_path)
            modes = stat.filemode(file_stat.st_mode)
            size = file_stat.st_size
            time_mode = datetime.fromtimestamp(int(file_stat.st_mtime))
            time_mode_f = time_mode.strftime('%b %d %H:%M')
            print(f'{file} {size} {time_mode_f} {modes}')


def ls(flags: set, paths: list[str]) -> None:
    """
    Выводит имена файлов, расположенных в директориях paths.
    (Если paths - пусто, то в рабочей директории).

    Args:
        - flags - флаг. Возможен: l для подробного вывода
            в формате: Имя, размер, дата изменения, права доступа.
        - paths - пути директорий.

    Prints:
        str - Имена файлов.
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
