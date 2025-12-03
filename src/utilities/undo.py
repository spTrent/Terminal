import os
import shutil

from src.config.consts import FOR_UNDO_HISTORY
from src.config.exceptions import IncorrectFlag, IncorrectInput, NothingToUndo
from src.config.functions import normalize_path
from src.config.logger import main_logger


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
        raise IncorrectFlag('Для undo не поддерживаются флаги')
    if paths:
        raise IncorrectInput('Для undo не поддерживаются аргументы')
    if len(FOR_UNDO_HISTORY) == 0:
        raise NothingToUndo('Нечего отменять')
    command, flag, paths = FOR_UNDO_HISTORY.pop()
    if command == 'cp':
        dest_path = normalize_path(paths[-1])
        if 'r' in flag or 'recursive' in flag:
            shutil.rmtree(dest_path)
        else:
            os.remove(dest_path)
    else:
        try:
            for file_path, dest_path in paths:
                if os.path.exists(file_path):
                    print(f'{file_path} пропущен: уже существует')
                    main_logger.error(f'{file_path} пропущен: уже существует')
                else:
                    shutil.move(dest_path, file_path)
        except FileNotFoundError:
            print(f'{file_path} удален')
            main_logger.error(f'{file_path} удален')
