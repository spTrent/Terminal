import os
import re

import src.config.functions
import src.config.logger


def find_all_files(path: str, files: list | None = None) -> list[str]:
    """
    Рекурсивно находит все файлы в директории.

    Args:
        path: Путь к директории для поиска.
        files: файлы текущей директории (используется для рекурсии).

    Returns:
        files: Список абсолютных путей ко всем файлам в директории.
    """
    if not files:
        files = []
    for file in os.listdir(path):
        file = os.path.join(path, file)
        if os.path.isdir(file):
            files.extend(find_all_files(file))
        else:
            files.append(file)
    return files


def find_in_file(path: str, pattern: str, flags: set) -> None:
    """
    Ищет pattern в файле и выводит совпадающие строки с номерами.

    Поддерживает регулярные выражения и простой поиск подстроки.

    Args:
        path: Путь к файлу для поиска.
        pattern: Паттерн поиска (может быть regex или строка).
        Должен быть записан в кавычках.
        flags: Набор флагов ('i'/'ignore-case' для поиска без учета регистра,
                            'r'/'recursive' для рекурсивного поиска).

    Prints:
        Строки, содержащие pattern с номерами.

    """
    flag = re.IGNORECASE if ('i' in flags or 'ignore-case' in flags) else 0
    try:
        re.compile(pattern, flag)
        reg = True
    except re.error:
        reg = False
    try:
        with open(path, 'r') as f:
            for n, row in enumerate(f.readlines(), start=1):
                if pattern and reg and re.search(pattern, row, flag):
                    print(f'{path}: {n} {row}', end='')
                elif pattern and not reg:
                    if flag:
                        pattern = pattern.lower()
                        row = row.lower()
                    if pattern in row:
                        print(f'{path}: {n} {row}', end='')

    except UnicodeDecodeError:
        print(f'{path} невозможно прочитать')
        src.config.logger.main_logger.info(f'{path} невозможно прочитать')
    except PermissionError:
        print(f'Нет прав на чтение {path}')
        src.config.logger.main_logger.info(f'Нет прав на чтение {path}')


def grep(flags: set, paths: list) -> None:
    """
    Ищет паттерн в файлах.

    Поддерживает рекурсивный поиск и поиск без учета регистра.

    Args:
        flags: множество флагов:
            - 'r'/'recursive': рекурсивный поиск в поддиректориях
            - 'i'/'ignore-case': поиск без учета регистра
        paths: Список паттерн + пути для поиска

    Prints:
        строки, содержащие pattern с номерами

    Raises:
        IncorrectFlag: Если указан неверный флаг
        PathError: Если указан несуществующий файл
    """
    src.config.functions.is_correct_flag(
        flags, {'r', 'i', 'ignore-case', 'recursive'}
    )
    pattern = ''
    if not os.path.exists(paths[0]):
        pattern = paths[0]
        paths = paths[1:]
    all_files = []
    for path in paths:
        path = src.config.functions.normalize_path(path)
        if os.path.isdir(path) and ('r' in flags or 'recursive' in flags):
            all_files.extend(find_all_files(path))
        else:
            all_files.append(path)
    for file in all_files:
        find_in_file(file, pattern, flags)
