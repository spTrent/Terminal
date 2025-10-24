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
