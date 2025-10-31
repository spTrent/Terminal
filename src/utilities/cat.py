import src.config.exceptions
import src.config.functions
import src.config.logger


def cat(flags: set, paths: list[str]) -> None:
    """
    Выводит содержимое файлов.

    Args:
        flags: Флаг утилиты. Должен быть пустым.
        paths: Список путей. Должен содержать хотя бы один файл.

    Prints:
        Печатает содержимое файлов.

    Raises:
        IncorrectFlag: Если указан флаг.
        IncorrectInput: Если список paths пуст.
        PathError: Если указанный путь не существует.
        IsNotFile: Если путь указывает на директорию.
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
            with open(path, 'r', encoding='utf-8') as f:
                cont = f.read().strip()
                if cont:
                    print(cont)

        except UnicodeDecodeError:
            print(f'{file} невозможно прочитать')
            src.config.logger.main_logger.info(f'{file} невозможно прочитать')
        except PermissionError:
            print(f'Нет прав на чтение {file}')
            src.config.logger.main_logger.info(f'Нет прав на чтение {file}')
