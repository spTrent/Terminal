from src.config.exceptions import IncorrectFlag, IncorrectInput
from src.config.functions import is_correct_file, normalize_path


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
        raise IncorrectFlag('Для cat не поддерживаются флаги')
    if not paths:
        raise IncorrectInput('Не указан файл для чтения')
    for file in paths:
        path: str = normalize_path(file)
        is_correct_file(path)
        with open(path, 'r', encoding='utf-8') as f:
            cont = f.read().strip()
            if cont:  # Нужна, чтобы при вызове на cat на
                # пустой файл не было пустой строки между вызовами
                print(cont)
