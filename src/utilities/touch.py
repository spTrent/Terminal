from src.config.exceptions import AlreadyExists, IncorrectFlag, PathError
from src.config.functions import (
    resolve_file_path,
)
from src.config.logger import main_logger


def touch(flag: set, paths: list) -> None:
    """
    Создаёт пустые файлы.

    Если файл уже существует, выводит сообщение и пропускает.

    Args:
        flag: Флаг утилиты. Должен быть пустым.
        paths: Список путей для создаваемых файлов.

    Returns:
        None.

    Raises:
        IncorrectFlag: Если указаны флаги.
    """
    if flag:
        raise IncorrectFlag('Для touch не поддерживаются флаги')
    for file in paths:
        try:
            dest = resolve_file_path('', file)
            with open(dest, 'w'):
                pass
        except PermissionError:
            print(f'Нет прав на создание {file}')
            main_logger.error(f'Нет прав на создание {file}')
        except AlreadyExists:
            print(f'{file} пропущен: уже существует')
            main_logger.error(f'{file} пропущен: уже существует')
        except PathError as msg:
            print(f'{file} пропущен: {msg}')
            main_logger.error(f'{file} пропущен: {msg}')
