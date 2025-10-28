import os
import shutil

import src.config.consts
import src.config.exceptions
import src.config.functions


def mv(flags: str, paths: list[str]) -> None:
    """
    Перемещает(переименовывает) файлы paths[:-1] в paths[-1].

    Args:
        - flags - флаг. Должен быть пустым для этой утилиты.
        - paths - пути к файлам. Должно быть хотя бы 2.

    Returns:
        None
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
            file = src.config.functions.normalize_path(file)
            file_name = file.split(os.sep)[-1]
            if os.path.isfile(file):
                dest_path = src.config.functions.resolve_file_path(
                    file_name, dest_path
                )
            else:
                dest_path = src.config.functions.resolve_file_path(
                    file_name, dest_path
                )
            shutil.move(file, dest_path)
            moved.append((file, dest_path))
        except PermissionError:
            print('Ошибка: Недостаточно прав')
        except src.config.exceptions.AlreadyExists:
            file_name = file.split(os.sep)[-1]
            print(f'{file_name} уже существует, пропущен')
    src.config.consts.FOR_UNDO_HISTORY.append(['mv', flags, moved])
