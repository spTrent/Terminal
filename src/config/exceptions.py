class TerminalException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class PathError(TerminalException):
    """Исключение неверного пути"""

    pass


class IncorrectInput(TerminalException):
    """Исключение неверного ввода"""

    pass


class IncorrectCommand(TerminalException):
    """Исключение неверной команды"""

    pass


class IsNotDirectory(TerminalException):
    """Исключение выполнения операции для директорий не над директорией"""

    pass


class IsNotFile(TerminalException):
    """Исключение выполнения операции для файлов не над файлами"""

    pass


class IsNotArchive(TerminalException):
    """Исключение выполнения операции для архивов не над архивами"""

    pass


class IncorrectFlag(TerminalException):
    """Исключение неверного ввода флага"""

    pass


class NothingToUndo(TerminalException):
    """Исключение выполнения undo, когда не осталось действий для отмены"""

    pass


class AlreadyExists(TerminalException):
    """Исключение создания файла с существующим именем"""

    pass
