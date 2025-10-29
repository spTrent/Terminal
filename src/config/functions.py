import os
import shlex

import src.config.consts
import src.config.exceptions


def resolve_file_path(file: str, path: str) -> str:
    """
    Преобразует path для команд, создающих файлы.

    Проверяет является ли путь абсолютным:
    Если да, то в path добавляется имя файла.
    Если нет, то проверяет, не пытается ли пользователь
    создать файл с существующим именем.

    Если path не существует, значит пользователь
    хочет создать файл с новым именем
    (или в несуществующую папку (исключение)).

    Проверяет path без file в конце на существование и корректность.
    Если все правильно - возвращает path.

    Args:
        file - имя копируемого файла.
        path(str) - путь, куда нужно скопировать.

    Returns:
        str - преобразованный path.
    """
    path = path.rstrip(os.sep)
    path = path.replace('~', os.path.expanduser('~'))
    if os.path.exists(path) and os.path.isabs(path) and os.path.isdir(path):
        return os.path.join(path, file)
    elif os.path.exists(path) and os.path.isdir(path):
        return os.path.join(os.getcwd(), path, file)
    elif os.path.exists(path):
        raise src.config.exceptions.AlreadyExists(
            f'Файл {path} уже существует'
        )
    else:
        dir_path = os.sep.join(path.split(os.sep)[:-1])
        if not dir_path:
            return os.path.join(os.getcwd(), path)
        dir_path = normalize_path(dir_path)
        is_correct_directory(dir_path)
        return path


def normalize_path(path: str) -> str:
    """
    Приводит путь path к абсолютному.

    Проверяет, существует ли путь. Если да, то проверяет на абсолютность.
    Если абсолютен, то оставляет. Если нет, то приводит к абсолютному.
    Бросает исключение PathError, если путь не существует.

    Args:
        path(str) - исходный путь

    Returns:
        abs_path(str) -> абсолютный путь.
    """
    path = path.replace('~', os.path.expanduser('~'))
    if os.path.exists(path) and os.path.isabs(path):
        return path
    elif os.path.exists(path):
        return os.path.join(os.getcwd(), path)
    else:
        raise src.config.exceptions.PathError(
            f'Не существует указанного пути {path}'
        )


def is_correct_directory(path: str) -> bool:
    """
    Приверяет директорию на корректность.

    Считает, что на вход подается существующий путь.
    Если директория - возвращает True.
    Иначе - бросает исключение IsNotDirectory.

    Args:
        path(str) - исходный путь.

    Returns:
        bool - ответ на вопрос: Это директория?
    """
    if os.path.isdir(path):
        return True
    raise src.config.exceptions.IsNotDirectory(f'{path} - не директория')


def is_correct_file(path: str) -> bool:
    """
    Приверяет файл на корректность.

    Считает, что на вход подается существующий путь.
    Если файл - возвращает True. Иначе - бросает исключение IsNotFile.

    Args:
        path(str) - исходный путь.

    Returns:
        bool - ответ на вопрос: Это файл?
    """
    if os.path.isfile(path):
        return True
    raise src.config.exceptions.IsNotFile(f'{path} - не файл')


def tokenize(stdin: str) -> tuple[str, set, list[str]]:
    """
    Токенизирует входную строку stdin.

    Разбивает строку на имена файлов, флаги и команды. Игнорирует пробелы.

    Args:
        stdin(str) - исходная строка.

    Returns:
        list(str, list(str)) - список вида [команда, ее аргументы]
    """
    # PATTERN = re.compile(r"'.*'|\S+|[a-zA-Z]+|--[a-zA-Z-]*|-[a-zA-Z]*")
    # tokens: list[str] = re.findall(PATTERN, stdin)
    tokens = shlex.split(stdin)
    command, *args = tokens
    flags, paths = set(), []
    if command not in src.config.consts.UTILITIES:
        raise src.config.exceptions.IncorrectCommand(
            f'Неизвестная команда {command}'
        )
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
    for f in flag:
        if f not in allowed_flags:
            raise src.config.exceptions.IncorrectFlag(f'Неправильный флаг {f}')
    return True
