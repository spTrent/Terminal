import os
import shutil

import src.config.consts
import src.config.exceptions
import src.config.functions
from src.utilities.cp import cp


def is_trash_empty(file_name: str) -> None:
    trash_file = os.path.join(src.config.consts.TRASH_PATH, file_name)
    if os.path.exists(trash_file) and os.path.isfile(trash_file):
        os.remove(trash_file)
    elif os.path.exists(trash_file):
        shutil.rmtree(trash_file)
    else:
        pass


def rm(flags: set, paths: list[str]) -> None:
    """
    Удаляет файлы(директории) указанные в paths.

    Args:
        - flags - флаг. Пустой для файлов, 'r' для директорий.
        - paths - пути к файлам. Должен быть хотя бы 1.

    Returns:
        None
    """

    src.config.functions.is_correct_flag(flags, {'r', 'recursive'})
    if not paths:
        raise src.config.exceptions.IncorrectInput(
            'Не указан файл для удаления'
        )
    removed = []
    for file in paths:
        file = src.config.functions.normalize_path(file)
        file_name = file.split(os.sep)[-1]
        file_trash = os.path.join(src.config.consts.TRASH_PATH, file_name)
        try:
            if flags:
                src.config.functions.is_correct_directory(file)
                if file in os.getcwd():
                    raise src.config.exceptions.TerminalException(
                        f'Ошибка: нет прав на удаление {file}'
                    )
                approve = input(f'Удалить {file}? [y / n]')
                if approve.lower() == 'y':
                    is_trash_empty(file_trash)
                    cp({'r'}, [file, file_trash])
                    shutil.rmtree(file)
            else:
                src.config.functions.is_correct_file(file)
                is_trash_empty(file_trash)
                cp(set(), [file, file_trash])
                os.remove(file)
            removed.append((file, file_trash))
        except PermissionError:
            print(f'Ошибка: нет прав на удаление {file}')
    src.config.consts.FOR_UNDO_HISTORY.append(['rm', flags, removed])
