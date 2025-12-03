import os

from src.config.exceptions import AlreadyExists, IncorrectFlag, PathError
from src.config.functions import resolve_file_path
from src.config.logger import main_logger


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
        raise IncorrectFlag('Для mkdir не поддерживаются файлы')
    for file in paths:
        try:
            dest = resolve_file_path('', file)
            if not os.path.exists(dest):
                os.mkdir(dest)
            else:
                print(f'{file} пропущен: уже существует')
                main_logger.error(f'{file} пропущен: уже существует')
        except PermissionError:
            print(f'Нет прав на создание {file}')
            main_logger.error(f'Нет прав на создание {file}')
        except AlreadyExists:
            print(f'{file} пропущен: уже существует')
            main_logger.error(f'{file} пропущен: уже существует')
        except PathError as msg:
            print(f'{file} пропущен: {msg}')
            main_logger.error(f'{file} пропущен: {msg}')
