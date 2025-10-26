import os
import re
import stat
from datetime import datetime

import src.exceptions
from src.utilities import utilities


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
        raise src.exceptions.IsNotDirectory(f'Файл {path} уже существует')
    else:
        dir_path = os.sep.join(path.split(os.sep)[:-1])
        if not dir_path:
            return path
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
        raise src.exceptions.PathError(f'Не существует указанного пути {path}')


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
    raise src.exceptions.IsNotDirectory(f'{path} - не директория')


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
    raise src.exceptions.IsNotFile(f'{path} - не файл')


def tokenize(stdin: str) -> tuple[str, str, list[str]]:
    """
    Токенизирует входную строку stdin.

    Разбивает строку на имена файлов, флаги и команды. Игнорирует пробелы.

    Args:
        stdin(str) - исходная строка.

    Returns:
        list(str, list(str)) - список вида [команда, ее аргументы]
    """
    PATTERN = re.compile(r"'.*'|\S+|[a-zA-Z]+|-[a-zA-Z]")
    tokens: list[str] = re.findall(PATTERN, stdin)
    command, *args = tokens
    flag, paths = '', []
    if command not in utilities:
        raise src.exceptions.IncorrectCommand(f'Неизвестная команда {command}')
    if args:
        if args[0].startswith('-'):
            flag = args[0][1:]
            paths = args[1:]
        else:
            flag = ''
            paths = args
    return (command, flag, paths)


def output(path: str) -> None:
    """
    Выводит файлы, расположенные в path, игнорируя скрытые.

    Args:
        path(str) - исходный путь.

    Returns:
        str - имена нескрытых файлов в path.
    """
    for file in os.listdir(path):
        if not file.startswith('.'):
            print(file, end=' ')
    print()


def detailed_output(path: str) -> None:
    """
    Выводит подробную информацию про файлы,
    расположенные в path, игнорируя скрытые.
    В формате: Имя Размер Время изменения Разрешения.

    Args:
        path(str) - исходный путь.

    Returns:
        str - информация про файлы, расположенные в path.
    """
    for file in sorted(os.listdir(path)):
        if not file.startswith('.'):
            file_path = os.path.join(path, file)
            file_stat = os.stat(file_path)
            modes = stat.filemode(file_stat.st_mode)
            size = file_stat.st_size
            time_mode = datetime.fromtimestamp(int(file_stat.st_mtime))
            time_mode_f = time_mode.strftime('%b %d %H:%M')
            print(f'{file} {size} {time_mode_f} {modes}')


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
    raise src.exceptions.IsNotArchive(f'{path} - не архив.')


def is_correct_flag(flag: set, allowed_flags: set) -> bool:
    for f in flag:
        if f not in allowed_flags:
            raise src.exceptions.IncorrectFlag(f'Неправильный флаг {f}')
    return True
