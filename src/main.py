import os
import shutil

import src.config.consts
import src.config.exceptions
import src.config.functions
import src.config.logger


def main() -> None:
    with open(src.config.consts.HISTORY_PATH, 'r') as f:
        history_lines = len(f.readlines())
    while 1:
        try:
            current_dir = os.getcwd().replace(os.path.expanduser('~'), '~')
            stdin = input(f'{current_dir}$ ')
            with open(src.config.consts.HISTORY_PATH, 'a') as f:
                f.write(f'{history_lines + 1} {stdin}\n')
            history_lines += 1
            src.config.logger.main_logger.info(stdin)
            if not stdin or stdin == 'stop':
                break
            command, flags, paths = src.config.functions.tokenize(stdin)
            if command in ['zip', 'tar', 'unzip', 'untar']:
                src.config.consts.UTILITIES[command](command, flags, paths)
            else:
                src.config.consts.UTILITIES[command](flags, paths)
            src.config.logger.main_logger.info('Success')

        except src.config.exceptions.TerminalException as message:
            print(f'{type(message).__name__}: {message}')
            src.config.logger.main_logger.error(message)
    shutil.rmtree(src.config.consts.TRASH_PATH)


if __name__ == '__main__':
    main()
