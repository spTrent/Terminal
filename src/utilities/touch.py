import src.config.exceptions
import src.config.functions
import src.config.logger


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
        raise src.config.exceptions.IncorrectFlag(
            'Для touch не поддерживаются флаги'
        )
    for file in paths:
        try:
            dest = src.config.functions.resolve_file_path('', file)
            with open(dest, 'w'):
                pass
        except PermissionError:
            print(f'Нет прав на создание {file}')
            src.config.logger.main_logger.error(f'Нет прав на создание {file}')
        except src.config.exceptions.AlreadyExists:
            print(f'{file} пропущен: уже существует')
            src.config.logger.main_logger.error(
                f'{file} пропущен: уже существует'
            )
