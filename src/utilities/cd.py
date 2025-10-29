import os

import src.config.exceptions
import src.config.functions


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
        raise src.config.exceptions.IncorrectFlag(
            'Для cd не поддерживаются флаги'
        )
    if len(paths) > 1:
        raise src.config.exceptions.IncorrectInput(
            'Слишком много аргументов для cd'
        )
    paths = paths if paths else ['~']
    path = src.config.functions.normalize_path(paths[0])
    src.config.functions.is_correct_directory(path)
    os.chdir(path)
