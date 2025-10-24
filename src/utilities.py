import os
import shutil

import src.exceptions
import src.functions


def ls(args: list) -> None:
    """
    Выводит имена файлов, расположенных в указанном пути.
    (Если args - пусто, то в рабочей директории).

    Args:
        args(list) - список аргументов.
        Возможные:
            Флаг -l и путь.

    Returns:
        str - Имена файлов.
    """
    if len(args) == 0:
        src.functions.output(os.getcwd())
    elif len(args) == 1 and args[0] == '-l':
        src.functions.detailed_output(os.getcwd())
    elif len(args) == 1:
        path: str = args[0]
        path = src.functions.normalize_path(path)
        src.functions.is_correct_directory(path)
        src.functions.output(path)
    else:
        raise src.exceptions.IncorrectInput(
            f'Слишком много аргументов для ls ({len(args)})'
        )


def cd(args: list) -> None:
    """
    Перемещает рабочую директорию.

    Args:
        args(list) - список аргументов.
        Возможные и Необходимые:
            Путь - новая рабочая директория.

    Returns:
        None
    """
    if len(args) > 1:
        raise src.exceptions.IncorrectInput(
            f'Слишком много аргументов для cd ({len(args)})'
        )
    path: str = args[0]
    path = src.functions.normalize_path(path)
    src.functions.is_correct_directory(path)
    os.chdir(path)


def cat(args: list) -> None:
    """
    Выводит содержимое файлов, указанных в аргументах.

    Args:
        args(list) - список аргументов.
        Возможные и Необходимые:
            Пути файлов. (Хотя бы один).

    Returns:
        str - содержимое файлов.
    """
    if len(args) == 0:
        raise src.exceptions.IncorrectInput('Нет файла для вывода содержимого')
    for file in args:
        path: str = src.functions.normalize_path(file)
        src.functions.is_correct_file(path)
        with open(path, 'r') as f:
            print(f.read())


def cp(args: list) -> None:
    """
    Копирует содержимое файла(директории) в указанный путь.

    Args:
        args(list) - список аргументов.
        Возможные:
            Флаг -r (для директорий).
        Необходимые:
            Путь 1 - путь файла.
            Путь 2 - путь назначения.


    Returns:
        str - Имена файлов.
    """
    print(args)
    try:
        if len(args) == 2:
            path_file = src.functions.normalize_path(args[0])
            file_name = path_file.split(os.sep)[-1]
            path_dest = src.functions.file_path_cp_mv(file_name, args[1])
            src.functions.is_correct_file(path_file)
            shutil.copy(path_file, path_dest)
        elif len(args) == 3:
            if args[0] == '-r':
                path_file = src.functions.normalize_path(args[1])
                dir_name = path_file.split(os.sep)[-1]
                path_dest = src.functions.dir_path_cp_mv(dir_name, args[2])
                src.functions.is_correct_directory(path_file)
                shutil.copytree(path_file, path_dest, dirs_exist_ok=True)
            else:
                raise src.exceptions.IncorrectInput(
                    f'Неверный флаг для cp: {args[0]}'
                )
        else:
            raise src.exceptions.IncorrectInput(
                f'Неверное количество аргументов для cp ({len(args)})'
            )
    except PermissionError:
        print('Ошибка: Недостаточно прав')


def mv(args: list) -> None:
    """
    Перемещает(переименовывает) файл в указанный путь.

    Args:
        args(list) - список аргументов.
        Возможные и Необходимые:
            Путь 1 - путь файла.
            Путь 2 - путь назначения.

    Returns:
        str - Имена файлов.
    """
    try:
        if len(args) != 2:
            raise src.exceptions.IncorrectInput(
                f'Неверное количество аргументов для mv ({len(args)})'
            )
        path_file = src.functions.normalize_path(args[0])
        file_name = path_file.split(os.sep)[-1]
        if os.path.isfile(path_file):
            path_dest = src.functions.file_path_cp_mv(file_name, args[1])
        else:
            path_dest = src.functions.dir_path_cp_mv(file_name, args[1])
        shutil.move(path_file, path_dest)
    except PermissionError:
        print('Ошибка: Недостаточно прав')


def rm(args: list) -> None:
    """
    Удаляет файлы(директории) указанные в аргументах.

    Args:
        args(list) - список аргументов.
        Возможные:
            Флаг -r (для директорий).
        Необходимые:
            Пути файлов. (Хотя бы один).


    Returns:
        str - Имена файлов.
    """
    try:
        if len(args) == 1:
            path = src.functions.normalize_path(args[0])
            src.functions.is_correct_file(path)
            approve = input(f'Удалить {path}? [y / n]')
            if approve == 'y':
                os.remove(path)
        elif len(args) == 2:
            if args[0] != '-r':
                raise src.exceptions.IncorrectInput('Неверный флаг для rm')
            path = src.functions.normalize_path(args[1])
            if path in os.getcwd():
                raise src.exceptions.TerminalException(
                    'Ошибка: Недостаточно прав'
                )
            src.functions.is_correct_directory(path)
            approve = input(f'Удалить {path}? [y / n]')
            if approve == 'y':
                shutil.rmtree(path)
        else:
            raise src.exceptions.IncorrectInput(
                f'Неверное количество аргументов для rm ({len(args)})'
            )
    except PermissionError:
        print('Ошибка: Недостаточно прав')


utilities = {
    'ls': ls,
    'cd': cd,
    'cat': cat,
    'cp': cp,
    'mv': mv,
    'rm': rm,
}
