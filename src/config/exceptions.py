class TerminalException(Exception):
    """Базовое исключение для терминала"""

    pass


class PathError(TerminalException):
    """Исключение неверного пути"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class IncorrectInput(TerminalException):
    """Исключение неверного ввода"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class IncorrectCommand(TerminalException):
    """Исключение неверной команды"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class IsNotDirectory(TerminalException):
    """Исключение выполнения операции для директорий не над директорией"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class IsNotFile(TerminalException):
    """Исключение выполнения операции для файлов не над файлами"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class IsNotArchive(TerminalException):
    """Исключение выполнения операции для архивов не над архивами"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class IncorrectFlag(TerminalException):
    """Исключение неверного ввода флага"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class NothingToUndo(TerminalException):
    """Исключение выполнения undo, когда не осталось действий для отмены"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class AlreadyExists(TerminalException):
    """Исключение создания файла с существующим именем"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
