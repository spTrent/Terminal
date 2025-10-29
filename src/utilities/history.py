import src.config.consts
import src.config.exceptions


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
    n = int(paths[0]) if paths else 0
    with open(src.config.consts.HISTORY_PATH, 'r') as history:
        commands = history.readlines()
        for command in commands[-n:]:
            print(command.strip())
