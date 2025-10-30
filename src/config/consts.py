import os
import shutil

FOR_UNDO_HISTORY: list[list] = []
HISTORY_PATH: str = os.path.join(os.path.expanduser('~'), '.history')
TRASH_PATH: str = os.path.join(os.path.expanduser('~'), '.trash')


def init_env() -> None:
    """
    Инициализирует окружение

    Если корзина уже существует, она очищается.
    Создаёт:
        - Файл истории команд (~/.history)
        - Директорию корзины (~/.trash)

    Returns:
        None
    """
    global FOR_UNDO_HISTORY
    FOR_UNDO_HISTORY.clear()
    if not os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, 'w'):
            pass
    if os.path.exists(TRASH_PATH):
        shutil.rmtree(TRASH_PATH)
    os.mkdir(TRASH_PATH)
