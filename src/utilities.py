import os
import shutil
from typing import Callable

import src.exceptions
import src.functions

for_undo_history = []
history_path = os.path.join(os.getcwd(), 'src/.history')
trash_path = os.path.join(os.getcwd(), 'src/.trash')
os.mkdir(trash_path)


def ls(flag: str, paths: list[str]) -> None:
    """
    Выводит имена файлов, расположенных в директориях paths.
    (Если paths - пусто, то в рабочей директории).

    Args:
        - flag - флаг. Возможен: l для подробного вывода
            в формате: Имя, размер, дата изменения, права доступа.
        - paths - пути директорий.

    Prints:
        str - Имена файлов.
    """
    paths = paths if paths else [os.getcwd()]
    for path in paths:
        path = src.functions.normalize_path(path)
        src.functions.is_correct_directory(path)
        print(f'{path.split(os.sep)[-1]}: ')
        if flag and flag == 'l':
            src.functions.detailed_output(path)
        elif flag:
            raise src.exceptions.IncorrectFlag(
                f'Неверный флаг для ls ({flag})'
            )
        else:
            src.functions.output(path)
        print()


def cd(flag: str, paths: list[str]) -> None:
    """
    Перемещает рабочую директорию.

    Args:
        - flag - флаг. Должен быть пустым для этой утилиты.
        - paths - путь новой рабочей директории. Должен быть 1.

    Returns:
        None
    """
    if flag:
        raise src.exceptions.IncorrectFlag('Для cd не поддерживаются флаги')
    if len(paths) > 1:
        raise src.exceptions.IncorrectInput('Слишком много аргументов для cd')
    path = src.functions.normalize_path(paths[0])
    src.functions.is_correct_directory(path)
    os.chdir(path)


def cat(flag: str, paths: list[str]) -> None:
    """
    Выводит содержимое файлов, указанных в path.

    Args:
        - flag - флаг. Должен быть пустым для этой утилиты.
        - paths - пути к файлам. Должен быть хотя бы 1.

    Prints:
        str - содержимое файлов.
    """
    if flag:
        raise src.exceptions.IncorrectFlag('Для cat не поддерживаются флаги')
    if not paths:
        raise src.exceptions.IncorrectInput('Не указан файл для чтения')
    for file in paths:
        path: str = src.functions.normalize_path(file)
        src.functions.is_correct_file(path)
        with open(path, 'r') as f:
            print(f.read())


def cp(flag: str, paths: list[str]) -> None:
    """
    Копирует содержимое файла(директории) paths[0] в указанный путь paths[1].

    Args:
        - flag - флаг. Пустой для файлов, 'r' для директорий.
        - paths - пути копируемой и скопированной директорий. Должно быть 2.

    Returns:
        None
    """
    if len(paths) != 2:
        src.exceptions.IncorrectInput('Неверное количество путей для cp')
    file_path = src.functions.normalize_path(paths[0])
    file_name = file_path.split(os.sep)[-1]
    dest_path = src.functions.resolve_file_path(file_name, paths[1])
    try:
        if flag and flag == 'r':
            src.functions.is_correct_directory(file_path)
            shutil.copytree(file_path, dest_path, dirs_exist_ok=True)
            for_undo_history.append(['cp', 'dir', file_path, dest_path])
        elif flag:
            raise src.exceptions.IncorrectFlag(f'Неверный флаг -{flag} для cp')
        else:
            src.functions.is_correct_file(file_path)
            shutil.copy(file_path, dest_path)
            for_undo_history.append(['cp', 'file', file_path, dest_path])
    except PermissionError:
        print('Ошибка: Недостаточно прав')


def mv(flag: str, paths: list[str]) -> None:
    """
    Перемещает(переименовывает) файлы paths[:-1] в paths[-1].

    Args:
        - flag - флаг. Должен быть пустым для этой утилиты.
        - paths - пути к файлам. Должно быть хотя бы 2.

    Returns:
        None
    """
    if flag:
        raise src.exceptions.IncorrectFlag('Для mv не поддерживаются флаги')
    if len(paths) < 2:
        raise src.exceptions.IncorrectInput(
            'Неверное количество аргументов для mv'
        )
    dest_path = paths[-1]
    try:
        for file in paths[:-1]:
            file = src.functions.normalize_path(file)
            file_name = file.split(os.sep)[-1]
            if os.path.isfile(file):
                dest_path = src.functions.resolve_file_path(
                    file_name, dest_path
                )
            else:
                dest_path = src.functions.resolve_file_path(
                    file_name, dest_path
                )
            shutil.move(file, dest_path)
    except PermissionError:
        print('Ошибка: Недостаточно прав')


def rm(flag: str, paths: list[str]) -> None:
    """
    Удаляет файлы(директории) указанные в paths.

    Args:
        - flag - флаг. Пустой для файлов, 'r' для директорий.
        - paths - пути к файлам. Должен быть хотя бы 1.

    Returns:
        None
    """
    if not paths:
        raise src.exceptions.IncorrectInput('Не указан файл для удаления')
    for file in paths:
        file = src.functions.normalize_path(file)
        try:
            if flag and flag == 'r':
                src.functions.is_correct_directory(file)
                if file in os.getcwd():
                    raise src.exceptions.TerminalException(
                        f'Ошибка: нет прав на удаление {file}'
                    )
                approve = input(f'Удалить {file}? [y / n]')
                if approve.lower() == 'y':
                    shutil.rmtree(file)
            elif flag:
                raise src.exceptions.IncorrectFlag(
                    f'Неверный флаг {flag} для rm'
                )
            else:
                src.functions.is_correct_file(file)
                approve = input(f'Удалить {file}? [y / n]')
                if approve.lower() == 'y':
                    os.remove(file)
        except PermissionError:
            print(f'Ошибка: нет прав на удаление {file}')


def make_archive(command: str, flag: str, paths: list[str]) -> None:
    """
    Создает архив из директории, указанной в args[0]
    в архив с именем args[1].

    Если command это zip, то формат .zip.
    Если command это tar, то формат .zip.gz

    Args:
        - command - формат сжатия.
        - flag - флаг. Должен быть пустым для этой утилиты.
        - paths - пути к архивируемой директории и архиву. Должно быть 2.

    Returns:
        None
    """
    if flag:
        raise src.exceptions.IncorrectFlag(
            f'Для {command} не поддерживаются флаги'
        )
    if len(paths) != 2:
        raise src.exceptions.IncorrectInput(
            f'Неверное количество аргументов для {command}'
        )
    dir_path = src.functions.normalize_path(paths[0])
    src.functions.is_correct_directory(dir_path)
    dir_name = dir_path.split(os.sep)[-1]
    dest_path = src.functions.resolve_file_path(dir_name, paths[1])
    if command == 'zip':
        shutil.make_archive(dest_path, 'zip', dir_path)
    else:
        shutil.make_archive(dest_path, 'gztar', dir_path)


def unpack(command: str, flag: str, paths: list[str]) -> None:
    """
    Распаковывает архив, указанный в paths[0].

    Проверяет, является ли файл архивом.
    Если да, то распаковывает.
    Если нет, то бросает исключение IsNotArchiveю.

    Args:
        - flag - флаг. Должен быть пустым для этой утилиты.
        - paths - путь к архиву. Должен быть 1.

    Returns:
        None
    """
    if flag:
        raise src.exceptions.IncorrectFlag(
            f'Для {command} не поддерживаются флаги'
        )
    if len(paths) != 1:
        raise src.exceptions.IncorrectInput(
            f'Неверное количество аргументов для {command}'
        )
    file_path = src.functions.normalize_path(paths[0])
    file = file_path.split(os.sep)[-1]
    file_name = file.split('.')[0]
    src.functions.is_archive(file_path)
    unzip_dest = os.path.join(os.getcwd(), file_name)
    shutil.unpack_archive(file_path, unzip_dest)


def history(args: list) -> None:
    n = 0
    if len(args) > 1:
        raise src.exceptions.IncorrectInput(
            f'Неверное количество аргументов для history ({len(args)})'
        )
    elif len(args) == 1:
        n = int(args[0])
    with open(history_path, 'r') as history:
        commands = history.readlines()
        for command in commands[-n:]:
            print(command.strip())


# def undo(args: list) -> None:
#     if len(args) != 0:
#         raise src.exceptions.IncorrectInput(
#             f'Неверное количество аргументов для undo ({len(args)})'
#         )
#     if len(for_undo_history) == 0:
#         raise src.exceptions.NothingToUndo('Нечего отменять')
#     command, file_type, file_path, dest_path = for_undo_history[-1]
#     if command == 'cp':
#         src.functions.cp_undo(file_type, dest_path)
#     else:
#         mv(dest_path, file_path)


utilities: dict[str, Callable] = {
    'ls': ls,
    'cd': cd,
    'cat': cat,
    'cp': cp,
    'mv': mv,
    'rm': rm,
    'history': history,
    # 'undo': undo,
    'zip': make_archive,
    'tar': make_archive,
    'unzip': unpack,
    'untar': unpack,
}

archivers: dict[str, Callable] = {
    'zip': make_archive,
    'tar': make_archive,
    'unzip': unpack,
    'untar': unpack,
}
