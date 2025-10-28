import os
import shutil

import src.config.exceptions
import src.config.functions


def is_archive(path: str) -> bool:
    """
    Проверяет, является ли path архивом.

    Args:
        path(str) - исходный путь к файлу.

    Returns:
        True, если архив. Исключение IsNotArchive, если не архив.
    """
    for exp in ['.zip', '.tar', '.tar.gz', '.tar.bz', '.tar.xz']:
        if path.endswith(exp):
            return True
    raise src.config.exceptions.IsNotArchive(f'{path} - не архив.')


def make_archive(command: str, flags: str, paths: list[str]) -> None:
    """
    Создает архив из директории, указанной в args[0]
    в архив с именем args[1].

    Если command это zip, то формат .zip.
    Если command это tar, то формат .tar.gz

    Args:
        - command - формат сжатия.
        - flags - флаг. Должен быть пустым для этой утилиты.
        - paths - пути к архивируемой директории и архиву. Должно быть 2.

    Returns:
        None
    """
    if flags:
        raise src.config.exceptions.IncorrectFlag(
            f'Для {command} не поддерживаются флаги'
        )
    if len(paths) != 2:
        raise src.config.exceptions.IncorrectInput(
            f'Неверное количество аргументов для {command}'
        )
    dir_path = src.config.functions.normalize_path(paths[0])
    src.config.functions.is_correct_directory(dir_path)
    dir_name = dir_path.split(os.sep)[-1]
    dest_path = src.config.functions.resolve_file_path(dir_name, paths[1])
    if command == 'zip':
        shutil.make_archive(dest_path, 'zip', dir_path)
    else:
        shutil.make_archive(dest_path, 'gztar', dir_path)


def unpack(command: str, flags: str, paths: list[str]) -> None:
    """
    Распаковывает архив, указанный в paths[0].

    Проверяет, является ли файл архивом.
    Если да, то распаковывает.
    Если нет, то бросает исключение IsNotArchiveю.

    Args:
        - flags - флаг. Должен быть пустым для этой утилиты.
        - paths - путь к архиву. Должен быть 1.

    Returns:
        None
    """
    if flags:
        raise src.config.exceptions.IncorrectFlag(
            f'Для {command} не поддерживаются флаги'
        )
    if len(paths) != 1:
        raise src.config.exceptions.IncorrectInput(
            f'Неверное количество аргументов для {command}'
        )
    file_path = src.config.functions.normalize_path(paths[0])
    file = file_path.split(os.sep)[-1]
    file_name = file.split('.')[0]
    is_archive(file_path)
    unzip_dest = os.path.join(os.getcwd(), file_name)
    shutil.unpack_archive(file_path, unzip_dest)
