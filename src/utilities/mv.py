import os
import shutil

from src.config.consts import FOR_UNDO_HISTORY
from src.config.exceptions import AlreadyExists, IncorrectFlag, IncorrectInput
from src.config.functions import normalize_path, resolve_file_path
from src.config.logger import main_logger


def mv(flags: set, paths: list[str]) -> None:
    """
    Перемещает или переименовывает файлы и директории.

    Args:
        flags: Флаг утилиты. Должен быть пустым.
        paths: Список из минимум 2 элементов:
            - paths[:-1]: файлы/директории для перемещения.
            - paths[-1]: директория назначения или новое имя.

    Returns:
        None.

    Raises:
        IncorrectFlag: Если указан флаг.
        IncorrectInput: Если указано меньше 2 путей.
        PathError: Если исходный путь не существует.
        AlreadyExists: Если целевой файл уже существует.
    """
    if flags:
        raise IncorrectFlag('Для mv не поддерживаются флаги')
    if len(paths) < 2:
        raise IncorrectInput('Неверное количество аргументов для mv')
    moved: list = []
    dest_path = paths[-1]
    for file in paths[:-1]:
        try:
            file_name = file.split(os.sep)[-1]
            resolved_path = resolve_file_path(file_name, dest_path)
            file = normalize_path(file)
            shutil.move(file, resolved_path)
            moved.append((file, resolved_path))
        except PermissionError:
            print('Ошибка: Недостаточно прав')
            main_logger.error(f'{file_name} пропущен: Недостаточно прав')

        except AlreadyExists as message:
            print(f'{file_name} пропущен: {message}')
            main_logger.error(f'{file_name} пропущен: {message}')
    if moved:
        FOR_UNDO_HISTORY.append(['mv', flags, moved])
