import pytest
from pathlib import Path
import src.config.functions
import src.config.exceptions
import src.config.utilities
import src.config.list_of_ut

def test_incorrect_command():
    with pytest.raises(src.config.exceptions.IncorrectCommand):
        src.config.functions.tokenize('go -r src')

def test_tokenize_long_flag():
    command, flag, paths = src.config.functions.tokenize('cp --recursive haha.txt test.txt')

    assert command == 'cp'
    assert isinstance(flag, set)
    assert 'recursive' in flag
    assert paths == ['haha.txt', 'test.txt']

def test_tokenize_flag():
    command, flag, paths = src.config.functions.tokenize('ls -a src tests')

    assert command == 'ls'
    assert isinstance(flag, set)
    assert 'a' in flag
    assert paths == ['src', 'tests']

def test_tokenize_without_flag():
    command, flag, paths = src.config.functions.tokenize('mv test.txt dest.txt')

    assert command == 'mv'
    assert isinstance(flag, set)
    assert not flag
    assert paths == ['test.txt', 'dest.txt']

def test_utilities_dict_exists():
    for ut in src.config.list_of_ut.UTILITIES:
        assert ut in src.config.utilities.UTILITIES

def test_init_env():
    src.config.consts.init_env()

    assert not src.config.consts.FOR_UNDO_HISTORY
    assert Path(src.config.consts.TRASH_PATH).exists()
    assert Path(src.config.consts.HISTORY_PATH).exists()
    assert not any(Path(src.config.consts.TRASH_PATH).iterdir())
