import os

import src.config.exceptions
import src.config.functions


def mkdir(flag: set, paths: list) -> None:
    if flag:
        raise src.config.exceptions.IncorrectFlag(
            'Для mkdir не поддерживаются файлы'
        )
    for file in paths:
        if os.path.exists(file):
            print(f'{file} уже существует')
            continue
        os.mkdir(file)
