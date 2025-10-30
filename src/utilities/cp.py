import os
import shutil

import src.config.consts
import src.config.exceptions
import src.config.functions
import src.config.logger


def cp(flags: set, paths: list[str]) -> None:
    """
    Копирует файлы и директории в указанное место.

    Args:
        flags: Множество флагов команды:
            - 'r' или 'recursive': для копирования директорий.
        paths: Список из двух элементов [источник, назначение]:
            - paths[0]: путь к копируемому файлу/директории.
            - paths[1]: путь назначения (директория или новое имя файла).

    Returns:
        None.

    Raises:
        IncorrectFlag: Если указан неправильный флаг.
        IncorrectInput: Если количество путей не равно 2.
        PathError: Если исходный путь не существует.
        IsNotFile: Если копируется файл с флагом r/recursive.
        IsNotDirectory: Если копируется директория без флага r/recursive.
        AlreadyExists: Если целевой файл уже существует.
    """
    src.config.functions.is_correct_flag(flags, {'r', 'recursive'})
    if len(paths) != 2:
        raise src.config.exceptions.IncorrectInput(
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
