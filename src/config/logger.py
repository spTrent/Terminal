import logging
import os

main_logger = logging.getLogger(__name__)
main_logger.setLevel(logging.INFO)
main_handler = logging.FileHandler(
    os.path.join('src', 'config', 'shell.log'), mode='a'
)
main_formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
)
main_handler.setFormatter(main_formatter)
main_logger.addHandler(main_handler)
