import os
import shutil

from src.config.consts import HISTORY_PATH, TRASH_PATH, init_env
from src.config.functions import tokenize
from src.config.logger import main_logger
from src.config.utilities import UTILITIES


def main() -> None:
    init_env()
    with open(HISTORY_PATH, 'r') as f:
        history_lines = len(f.readlines())
    current_dir = os.getcwd().replace(os.path.expanduser('~'), '~')
    while (stdin := input(f'{current_dir}$ ')) != 'exit':
        if not stdin:
            continue
        try:
            with open(HISTORY_PATH, 'a') as f:
                f.write(f'{history_lines + 1} {stdin}\n')
            history_lines += 1
            main_logger.info(stdin)
            command, flags, paths = tokenize(stdin)
            if command in ['zip', 'tar', 'unzip', 'untar']:
                UTILITIES[command](command, flags, paths)
            else:
                UTILITIES[command](flags, paths)
            main_logger.info('Success')
        except Exception as message:
            print(f'{type(message).__name__}: {message}')
            main_logger.error(message)
        finally:
            current_dir = os.getcwd().replace(os.path.expanduser('~'), '~')
    shutil.rmtree(TRASH_PATH)


if __name__ == '__main__':
    main()
