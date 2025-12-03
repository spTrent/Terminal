import os

from src.config.exceptions import IncorrectFlag, IncorrectInput
from src.config.functions import is_correct_directory, normalize_path


def cd(flags: set, paths: list[str]) -> None:
    """
    Меняет текущую рабочую директорию.

    Поддерживает специальные пути:
        '.' (текущая)
        '..' (родительская)
        '~' (домашняя)

    Args:
        flags: Флаг утилиты. Должен быть пустым.
        paths: Список из одного элемента - путь к новой рабочей директории.

    Returns:
        None.

    Raises:
        IncorrectFlag: Если указан флаг.
        IncorrectInput: Если указано больше одного пути.
        PathError: Если указанный путь не существует.
        IsNotDirectory: Если путь указывает на файл.
    """
    if flags:
        raise IncorrectFlag('Для cd не поддерживаются флаги')
    if len(paths) > 1:
        raise IncorrectInput('Слишком много аргументов для cd')
    paths = paths if paths else ['~']
    path = normalize_path(paths[0])
    is_correct_directory(path)
    os.chdir(path)
