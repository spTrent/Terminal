import os

import src.config.exceptions
import src.config.functions
import src.config.logger


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
        try:
            dest = src.config.functions.resolve_file_path('', file)
            if not os.path.exists(dest):
                os.mkdir(dest)
            else:
                print(f'{file} пропущен: уже существует')
                src.config.logger.main_logger.error(
                    f'{file} пропущен: уже существует'
                )
        except PermissionError:
            print(f'Нет прав на создание {file}')
            src.config.logger.main_logger.error(f'Нет прав на создание {file}')
        except src.config.exceptions.AlreadyExists:
            print(f'{file} пропущен: уже существует')
            src.config.logger.main_logger.error(
                f'{file} пропущен: уже существует'
            )
        except src.config.exceptions.PathError as msg:
            print(f'{file} пропущен: {msg}')
            src.config.logger.main_logger.error(f'{file} пропущен: {msg}')
