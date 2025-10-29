import os
import shutil

import src.config.consts
import src.config.exceptions
import src.config.functions
from src.utilities.mv import mv


def undo(flags: set, paths: list) -> None:
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
    command, flag, paths = src.config.consts.FOR_UNDO_HISTORY[-1]
    if command == 'cp':
        dest_path = src.config.functions.normalize_path(paths[-1])
        if 'r' in flag or 'recursive' in flag:
            shutil.rmtree(dest_path)
        else:
            os.remove(dest_path)
    else:
        for file_path, dest_path in paths:
            mv(set(), [dest_path, file_path])
