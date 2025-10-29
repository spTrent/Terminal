import os

import src.config.exceptions
import src.config.functions
import src.config.logger


def touch(flag: set, paths: list) -> None:
    if flag:
        raise src.config.exceptions.IncorrectFlag(
            'Для touch не поддерживаются флаги'
        )
    for file in paths:
        if not os.path.exists(file):
            with open(file, 'w'):
                pass
        else:
            print(f'{file} пропущен: уже существует')
            src.config.logger.main_logger.error(
                f'{file} пропущен: уже существует'
            )
