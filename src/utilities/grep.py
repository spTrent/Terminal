import os
import re

import src.config.functions


def find_all_files(path: str, files: list | None = None) -> list[str]:
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
    pattern = pattern[1:-1]
    flag = re.IGNORECASE if ('i' in flags or 'ignore-case' in flags) else 0
    try:
        with open(path, 'r') as f:
            for n, row in enumerate(f.readlines(), start=1):
                if pattern and re.search(pattern, row, flag):
                    print(f'{path}: {n} {row}', end='')
    except UnicodeDecodeError:
        pass


def grep(flags: set, paths: list) -> None:
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
