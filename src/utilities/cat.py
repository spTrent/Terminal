import src.config.exceptions
import src.config.functions
import src.config.logger


def cat(flags: set, paths: list[str]) -> None:
    """
    Выводит содержимое файлов, указанных в path.

    Args:
        - flags - флаг. Должен быть пустым для этой утилиты.
        - paths - пути к файлам. Должен быть хотя бы 1.

    Prints:
        str - содержимое файлов.
    """
    if flags:
        raise src.config.exceptions.IncorrectFlag(
            'Для cat не поддерживаются флаги'
        )
    if not paths:
        raise src.config.exceptions.IncorrectInput('Не указан файл для чтения')
    for file in paths:
        try:
            path: str = src.config.functions.normalize_path(file)
            src.config.functions.is_correct_file(path)
            with open(path, 'r') as f:
                print(f.read())
        except UnicodeDecodeError:
            print(f'{file} невозможно прочитать')
            src.config.logger.main_logger.info(f'{file} невозможно прочитать')
