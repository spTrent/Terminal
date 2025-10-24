import os

import src.exceptions
import src.functions
import src.logger
import src.utilities


def main() -> None:
    while 1:
        try:
            stdin = input(f'{os.getcwd()}$ ')
            src.logger.main_logger.info(stdin)
            if not stdin:
                break
            command, *args = src.functions.tokenize(stdin)
            # print(*args)
            src.utilities.utilities[command](*args)
            src.logger.main_logger.info('Success')

        except src.exceptions.TerminalException as message:
            print(f'{type(message).__name__}: {message}')
            src.logger.main_logger.error(message)


if __name__ == '__main__':
    main()
