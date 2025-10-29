import os

import src.config.exceptions
import src.config.functions


def mkdir(flag: set, paths: list) -> None:
    """
    Создаёт пустые директории.

    Если директория уже существует, выводит сообщение и пропускает.

    Args:
        flag: Флаг утилиты. Должен быть пустым.
        paths: Список путей для создаваемых директорий.

    Returns:
        None.

    Raises:
        IncorrectFlag: Если указаны флаги.
    """
    if flag:
        raise src.config.exceptions.IncorrectFlag(
            'Для mkdir не поддерживаются файлы'
        )
    for file in paths:
        if os.path.exists(file):
            print(f'{file} уже существует')
            continue
        os.mkdir(file)
