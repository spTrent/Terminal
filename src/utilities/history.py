import src.config.consts
import src.config.exceptions
import src.config.logger


def history(flags: set, paths: list) -> None:
    """
    Выводит историю выполненных команд.

    Args:
        flags: Флаг утилиты. Должен быть пустым.
        paths: Количество выводимых операций.

    Prints:
        Печатает историю вызова утилит.

    Raises:
        IncorrectFlag: Если указаны флаги.
        IncorrectInput: Если количество аргументов больше 1.
    """
    if flags:
        raise src.config.exceptions.IncorrectFlag(
            'Для history не поддерживаются флаги'
        )
    if len(paths) > 1:
        raise src.config.exceptions.IncorrectInput(
            'Неверное количество аргументов для history'
        )
    try:
        if paths and paths[0] == '0':
            return None
        n = int(paths[0]) if paths else 0
        with open(src.config.consts.HISTORY_PATH, 'r') as history:
            commands = history.readlines()
            for command in commands[-n:]:
                print(command.strip())
    except ValueError:
        print(f'Неправильный аргумент {paths[0]}')
        src.config.logger.main_logger.error(
            f'Неправильный аргумент {paths[0]}'
        )
