import src.config.consts
from src.config.exceptions import IncorrectFlag, IncorrectInput


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
        raise IncorrectFlag('Для history не поддерживаются флаги')
    if len(paths) > 1:
        raise IncorrectInput('Неверное количество аргументов для history')
    if paths and paths[0] == '0':
        return None
    n = int(paths[0]) if paths else 0
    with open(src.config.consts.HISTORY_PATH, 'r') as history:
        commands = history.readlines()
        for command in commands[-n:]:
            print(command.strip())
