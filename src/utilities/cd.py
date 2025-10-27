import os

import src.config.exceptions
import src.config.functions


def cd(flags: str, paths: list[str]) -> None:
    """
    Перемещает рабочую директорию.

    Args:
        - flags - флаг. Должен быть пустым для этой утилиты.
        - paths - путь новой рабочей директории. Должен быть 1.

    Returns:
        None
    """
    if flags:
        raise src.config.exceptions.IncorrectFlag(
            'Для cd не поддерживаются флаги'
        )
    if len(paths) > 1:
        raise src.config.exceptions.IncorrectInput(
            'Слишком много аргументов для cd'
        )
    path = src.config.functions.normalize_path(paths[0])
    src.config.functions.is_correct_directory(path)
    os.chdir(path)
