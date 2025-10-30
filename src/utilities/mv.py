import os
import shutil

import src.config.consts
import src.config.exceptions
import src.config.functions
import src.config.logger


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
        raise src.config.exceptions.IncorrectFlag(
            'Для mv не поддерживаются флаги'
        )
    if len(paths) < 2:
        raise src.config.exceptions.IncorrectInput(
            'Неверное количество аргументов для mv'
        )
    moved: list = []
    dest_path = paths[-1]
    for file in paths[:-1]:
        try:
            file_name = file.split(os.sep)[-1]
            resolved_path = src.config.functions.resolve_file_path(
                file_name, dest_path
            )
            file = src.config.functions.normalize_path(file)
            shutil.move(file, resolved_path)
            moved.append((file, resolved_path))
        except PermissionError:
            print('Ошибка: Недостаточно прав')
            src.config.logger.main_logger.error(
                f'{file_name} пропущен: Недостаточно прав'
            )

        except src.config.exceptions.AlreadyExists as message:
            print(f'{file_name} пропущен: {message}')
            src.config.logger.main_logger.error(
                f'{file_name} пропущен: {message}'
            )
    if moved:
        src.config.consts.FOR_UNDO_HISTORY.append(['mv', flags, moved])
