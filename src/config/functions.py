import os
import shlex

import src.config.list_of_ut
from src.config.exceptions import (
    AlreadyExists,
    IncorrectCommand,
    IncorrectFlag,
    IncorrectInput,
    IsNotDirectory,
    IsNotFile,
    PathError,
)


def resolve_file_path(file: str, path: str) -> str:
    """
    Преобразует путь назначения для утилит, которые создают файлы.

    Определяет, является ли путь директорией или новым именем файла.

    Args:
        file: Имя создаваемого файла.
        path: Путь назначения.

    Returns:
        Путь к создаваемому файлу.

    Raises:
        AlreadyExists: Если создаваемый файл уже существует.
        PathError: Если родительская директория не существует.
        IsNotDirectory: Если родительская директория не директория.
    """
    path = path.rstrip(os.sep)
    path = path.replace('~', os.path.expanduser('~'))
    if os.path.exists(path) and os.path.isabs(path) and os.path.isdir(path):
        return os.path.join(path, file)
    elif os.path.exists(path) and os.path.isdir(path):
        path = os.path.join(os.getcwd(), path, file)
        if os.path.exists(path) and os.path.isfile(path):
            raise AlreadyExists(f'{path} уже существует')
        return path
    elif os.path.exists(path):
        raise AlreadyExists(f'{path} уже существует')
    else:
        dir_path = os.sep.join(path.split(os.sep)[:-1])
        if not dir_path:
            return os.path.join(os.getcwd(), path)
        dir_path = normalize_path(dir_path)
        is_correct_directory(dir_path)
        return path


def normalize_path(path: str) -> str:
    """
    Приводит относительный путь к абсолютному и заменяет ~.

    Args:
        path: Исходный путь.

    Returns:
        Абсолютный путь.

    Raises:
        PathError: Если путь не существует.
    """
    path = path.replace('~', os.path.expanduser('~'))
    if os.path.exists(path) and os.path.isabs(path):
        return path
    elif os.path.exists(path):
        return os.path.join(os.getcwd(), path)
    else:
        raise PathError(f'Не существует указанного пути {path}')


def is_correct_directory(path: str) -> bool:
    """
    Проверяет, является ли путь директорией.

    Args:
        path: Путь для проверки.

    Returns:
        True, если путь является директорией.

    Raises:
        IsNotDirectory: Если путь не является директорией.
    """
    if os.path.isdir(path):
        return True
    raise IsNotDirectory(f'{path} - не директория')


def is_correct_file(path: str) -> bool:
    """
    Проверяет, является ли путь файлом.

    Args:
        path: Путь для проверки.

    Returns:
        True, если путь является файлом.

    Raises:
        IsNotFile: Если путь не является файлом.
    """
    if os.path.isfile(path):
        return True
    raise IsNotFile(f'{path} - не файл')


def tokenize(stdin: str) -> tuple[str, set, list[str]]:
    """
    Разбирает входную строку на команду, флаги и аргументы.

    Args:
        stdin: Строка от пользователя.

    Returns:
        Кортеж (команда, множество флагов, список путей).

    Raises:
        IncorrectCommand: Если введенная команда не поддерживается.
    """
    try:
        tokens = shlex.split(stdin)
    except ValueError:
        raise IncorrectInput('Неверный ввод') from None
    command, *args = tokens
    flags, paths = set(), []
    if command not in src.config.list_of_ut.UTILITIES:
        raise IncorrectCommand(f'Неизвестная команда {command}')
    if args:
        if args[0].startswith('--'):
            flags.add(args[0][2:])
            paths = args[1:]
        elif args[0].startswith('-'):
            flags = set(args[0][1:])
            paths = args[1:]
        else:
            flags = set()
            paths = args
    return (command, flags, paths)


def is_correct_flag(flag: set, allowed_flags: set) -> bool:
    """
    Проверяет корректность флагов команды.

    Args:
        flag: Множество флагов от пользователя.
        allowed_flags: Множество разрешённых флагов для команды.

    Returns:
        True, если все флаги корректны.

    Raises:
        IncorrectFlag: Если хотя бы один флаг недопустим.
    """
    for f in flag:
        if f not in allowed_flags:
            raise IncorrectFlag(f'Неправильный флаг {f}')
    return True
