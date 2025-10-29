import os
import shutil

import src.config.consts
import src.config.exceptions
import src.config.functions
import src.config.logger
from src.utilities.cp import cp


def is_trash_empty(file_name: str) -> None:
    """
    Очищает корзину от файла с таким же именем перед удалением.

    Args:
        file_name: Имя файла в корзине для удаления.

    Returns:
        None. Удаляет файл/директорию из корзины, если такая есть.
    """
    trash_file = os.path.join(src.config.consts.TRASH_PATH, file_name)
    if os.path.exists(trash_file) and os.path.isfile(trash_file):
        os.remove(trash_file)
    elif os.path.exists(trash_file):
        shutil.rmtree(trash_file)
    else:
        pass


def rm(flags: set, paths: list[str]) -> None:
    """
    Удаляет файлы/директории, перемещая в корзину.

    Файлы не удаляются навсегда, а перемещаются в ~/.trash
    для возможности восстановления через undo.
    Для директорий запрашивается подтверждение.

    Args:
        flags: Множество флагов:
            - 'r'/'recursive': удаление директорий.
        paths: Список путей для удаления.

    Returns:
        None.

    Raises:
        IncorrectFlag: Если указан неподдерживаемый флаг.
        IncorrectInput: Если не указаны файлы для удаления.
        TerminalException: При попытке удалить текущую/родительскую директорию.
        PathError: Если указан несуществующий путь.
        IsNotFile: При попытке удаления файла с флагом r/recursive.
        IsNotDirectory: При попытке удалить директорию без флага r/recursive.
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
                if os.path.samefile(
                    file, os.getcwd()
                ) or os.getcwd().startswith(file):
                    src.config.logger.main_logger.error(
                        f'{file_name} пропущен: недостаточно прав'
                    )
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
            print(f'Ошибка: нет прав на удаление {file_name}')
            src.config.logger.main_logger.error(
                f'{file_name} пропущен: недостаточно прав'
            )
    if removed:
        src.config.consts.FOR_UNDO_HISTORY.append(['rm', flags, removed])
