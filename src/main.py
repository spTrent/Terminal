import os
import shutil

import src.exceptions
import src.functions
import src.logger
import src.utilities


def main() -> None:
    with open(src.utilities.history_path, 'r') as f:
        history_lines = len(f.readlines())
    while 1:
        try:
            current_dir = os.getcwd().replace(os.path.expanduser('~'), '~')
            stdin = input(f'{current_dir}$ ')
            with open(src.utilities.history_path, 'a') as f:
                f.write(f'{history_lines + 1} {stdin}\n')
            history_lines += 1
            src.logger.main_logger.info(stdin)
            if not stdin or stdin == 'stop':
                break
            command, flag, paths = src.functions.tokenize(stdin)
            if command in ['zip', 'tar', 'unzip', 'untar']:
                src.utilities.archivers[command](command, flag, paths)
            else:
                src.utilities.utilities[command](flag, paths)
            src.logger.main_logger.info('Success')

        except src.exceptions.TerminalException as message:
            print(f'{type(message).__name__}: {message}')
            src.logger.main_logger.error(message)
    shutil.rmtree(src.utilities.trash_path)


if __name__ == '__main__':
    main()
