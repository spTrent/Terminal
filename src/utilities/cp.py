import os
import shutil

import src.config.consts
import src.config.exceptions
import src.config.functions
import src.config.logger


def cp(flags: set, paths: list[str]) -> None:
    """
    Копирует содержимое файла(директории) paths[0] в указанный путь paths[1].

    Args:
        - flags - флаг. Пустой для файлов, 'r' для директорий.
        - paths - пути копируемой и скопированной директорий. Должно быть 2.

    Returns:
        None
    """
    src.config.functions.is_correct_flag(flags, {'r', 'recursive'})
    if len(paths) != 2:
        src.config.exceptions.IncorrectInput(
            'Неверное количество путей для cp'
        )
    file_path = src.config.functions.normalize_path(paths[0])
    file_name = file_path.split(os.sep)[-1]
    dest_path = src.config.functions.resolve_file_path(file_name, paths[1])
    try:
        if flags:
            src.config.functions.is_correct_directory(file_path)
            shutil.copytree(file_path, dest_path, dirs_exist_ok=True)
        else:
            src.config.functions.is_correct_file(file_path)
            shutil.copy(file_path, dest_path)
        src.config.consts.FOR_UNDO_HISTORY.append(
            ['cp', flags, [file_path, dest_path]]
        )
    except PermissionError:
        print('Ошибка: Недостаточно прав')
        src.config.logger.main_logger.error(
            f'{file_name} пропущен: недостаточно прав'
        )
