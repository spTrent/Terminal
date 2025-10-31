import os
import tempfile
from pathlib import Path

import pytest

import src.config.consts
import src.config.exceptions
from src.utilities.history import history


class TestHistoryCommand:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.temp_history = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.original_history_path = src.config.consts.HISTORY_PATH
        src.config.consts.HISTORY_PATH = self.temp_history.name

        self.temp_history.write('ls\n')
        self.temp_history.write('cd /tmp\n')
        self.temp_history.write('touch file.txt\n')
        self.temp_history.write('mkdir newdir\n')
        self.temp_history.write('cat file.txt\n')
        self.temp_history.close()

        yield

        src.config.consts.HISTORY_PATH = self.original_history_path
        os.unlink(self.temp_history.name)

    def test_history_no_args(self, capsys):
        history(set(), [])
        captured = capsys.readouterr()

        assert 'ls' in captured.out
        assert 'cd /tmp' in captured.out
        assert 'touch file.txt' in captured.out
        assert 'cat file.txt' in captured.out
        assert 'mkdir newdir' in captured.out

    def test_history_show_all(self, capsys):
        history(set(), ['10'])
        captured = capsys.readouterr()

        assert 'ls' in captured.out
        assert 'cd /tmp' in captured.out
        assert 'touch file.txt' in captured.out
        assert 'mkdir newdir' in captured.out
        assert 'cat file.txt' in captured.out

    def test_history_show_last_n(self, capsys):
        history(set(), ['2'])
        captured = capsys.readouterr()

        assert 'mkdir newdir' in captured.out
        assert 'cat file.txt' in captured.out
        assert 'ls' not in captured.out
        assert 'cd /tmp' not in captured.out

    def test_history_show_last_one(self, capsys):
        history(set(), ['1'])
        captured = capsys.readouterr()

        assert captured.out == 'cat file.txt\n'

    def test_history_with_flag(self):
        with pytest.raises(src.config.exceptions.IncorrectFlag):
            history({'a'}, [])

    def test_history_too_many_args(self):
        with pytest.raises(src.config.exceptions.IncorrectInput):
            history(set(), ['5', '10'])

    def test_history_zero(self, capsys):
        history(set(), ['0'])
        captured = capsys.readouterr()

        assert not captured.out


    def test_history_many_commands(self, capsys):
        with open(src.config.consts.HISTORY_PATH, 'w') as f:
            for i in range(100):
                f.write(f'command_{i}\n')

        history(set(), [])
        captured = capsys.readouterr()

        assert 'command_0' in captured.out
        assert 'command_50' in captured.out
        assert 'command_99' in captured.out

    def test_history_many_commands_last_n(self, capsys):
        with open(src.config.consts.HISTORY_PATH, 'w') as f:
            for i in range(100):
                f.write(f'command_{i}\n')

        history(set(), ['10'])
        captured = capsys.readouterr()

        assert 'command_90' in captured.out
        assert 'command_99' in captured.out
        assert 'command_89' not in captured.out

    def test_history_float(self, capsys):
        history({}, ['14.1'])
        captured = capsys.readouterr()

        assert 'Неправильный аргумент 14.1' in captured.out

