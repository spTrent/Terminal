import os
import shutil

from src.config.exceptions import (
    AlreadyExists,
    IncorrectFlag,
    IncorrectInput,
    IsNotArchive,
)
from src.config.functions import is_correct_directory, normalize_path

zip = 'zip'
unzip = 'unzip'


def is_archive(path: str) -> bool:
    """
    Проверяет, является ли файл архивом поддерживаемого формата.

    Поддерживаемые форматы: .zip, .tar, .tar.gz, .tar.bz, .tar.xz.

    Args:
        path: Путь к файлу для проверки.

    Returns:
        True, если файл является архивом.

    Raises:
        IsNotArchive: Если файл не является архивом поддерживаемого формата.
    """
    for exp in ['.zip', '.tar', '.tar.gz', '.tar.bz', '.tar.xz']:
        if path.endswith(exp):
            return True
    raise IsNotArchive(f'{path} - не архив.')


def make_archive(command: str, flags: set, paths: list[str]) -> None:
    """
    Создаёт архив из указанной директории.

    Формат архива зависит от команды: 'zip' создаёт .zip, 'tar' создаёт .tar.gz

    Args:
        command: Формат архива ('zip' или 'tar').
        flags: Флаг утилиты. Должен быть пустым.
        paths: Список из двух элементов [путь_к_директории, имя_архива].

    Returns:
        None

    Raises:
        IncorrectFlag: Если указаны флаги.
        IncorrectInput: Если количество путей не равно 2.
        IsNotDirectory: Если исходный путь не является директорией.
        PathError: Если указан несуществующий файл.
    """
    if flags:
        raise IncorrectFlag(f'Для {command} не поддерживаются флаги')
    if len(paths) > 2:
        raise IncorrectInput(f'Неверное количество аргументов для {command}')
    dir_path = normalize_path(paths[0])
    is_correct_directory(dir_path)
    dest_path = paths[-1]
    if command == zip:
        shutil.make_archive(dest_path, 'zip', dir_path)
    else:
        shutil.make_archive(dest_path, 'gztar', dir_path)


def unpack(command: str, flags: set, paths: list[str]) -> None:
    """
    Распаковывает архив в текущую рабочую директорию, сохраняя имя.

    Args:
        command: Команда распаковки ('unzip' или 'untar').
        flags: Флаг утилиты. Должен быть пустым.
        paths: Список из одного элемента [путь_к_архиву].

    Returns:
        None

    Raises:
        IncorrectFlag: Если указаны флаги.
        IncorrectInput: Если количество путей не равно 1.
        IsNotArchive: Если файл не является архивом.
    """
    if flags:
        raise IncorrectFlag(f'Для {command} не поддерживаются флаги')
    if len(paths) != 1:
        raise IncorrectInput(f'Неверное количество аргументов для {command}')
    file_path = normalize_path(paths[0])
    file = file_path.split(os.sep)[-1]
    file_name = file[:-4] if command == unzip else file[:-7]
    is_archive(file)
    unzip_dest = os.path.join(os.getcwd(), file_name)
    if os.path.exists(unzip_dest):
        raise AlreadyExists(f'{unzip_dest} уже существует')
    if command == unzip:
        shutil.unpack_archive(file_path, unzip_dest)
    else:
        shutil.unpack_archive(file_path, unzip_dest, filter='data')
