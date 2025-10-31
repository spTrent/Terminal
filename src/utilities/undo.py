import os
import shutil

import src.config.consts
import src.config.exceptions
import src.config.functions


def undo(flags: set, paths: list) -> None:
    """
    Отменяет последнюю операцию cp/mv/rm.

    Args:
        flags: Флаг утилиты. Должен быть пустым.
        paths: Аргументы утилиты. Должны быть пустыми.

    Returns:
        None.

    Raises:
        IncorrectFlag: Если указаны флаги.
        IncorrectInput: Если указаны аргументы.
        NothingToUndo: Если нет операций для отмены.
    """
    if flags:
        raise src.config.exceptions.IncorrectFlag(
            'Для undo не поддерживаются флаги'
        )
    if paths:
        raise src.config.exceptions.IncorrectInput(
            'Для undo не поддерживаются аргументы'
        )
    if len(src.config.consts.FOR_UNDO_HISTORY) == 0:
        raise src.config.exceptions.NothingToUndo('Нечего отменять')
    command, flag, paths = src.config.consts.FOR_UNDO_HISTORY.pop()
    if command == 'cp':
        dest_path = src.config.functions.normalize_path(paths[-1])
        if 'r' in flag or 'recursive' in flag:
            shutil.rmtree(dest_path)
        else:
            os.remove(dest_path)
    else:
        try:
            for file_path, dest_path in paths:
                if os.path.exists(file_path):
                    print(f'{file_path} пропущен: уже существует')
                    src.config.logger.main_logger.error(
                        f'{file_path} пропущен: уже существует'
                    )
                else:
                    shutil.move(dest_path, file_path)
        except FileNotFoundError:
            print(f'{file_path} удален')
            src.config.logger.main_logger.error(f'{file_path} удален')
