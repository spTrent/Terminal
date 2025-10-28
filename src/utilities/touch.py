import os

import src.config.exceptions
import src.config.functions


def touch(flag: set, paths: list) -> None:
    if flag:
        raise src.config.exceptions.IncorrectFlag(
            'Для touch не поддерживаются флаги'
        )
    for file in paths:
        if os.path.exists(file):
            print(f'{file} уже существует')
        with open(file, 'w'):
            pass
