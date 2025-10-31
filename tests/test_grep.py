import os
import shutil
import tempfile
from pathlib import Path

import pytest

import src.config.exceptions
from src.utilities.grep import grep


class TestGrepCommand:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        Path(self.test_dir, 'file1.txt').write_text('Hello World\nPython\n')
        Path(self.test_dir, 'file2.txt').write_text('Goodbye World\nJava\n')
        
        subdir = Path(self.test_dir, 'subdir')
        subdir.mkdir()
        Path(subdir, 'file3.txt').write_text('Hello from subdir\n')
        
        yield
        
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_grep_file(self, capsys):
        grep(set(), ['Hello', 'file1.txt'])
        captured = capsys.readouterr()
        
        assert '1 Hello World' in captured.out
        assert 'Python' not in captured.out

    def test_grep_files(self, capsys):
        grep(set(), ['World', 'file1.txt', 'file2.txt'])
        captured = capsys.readouterr()
        
        assert '1 Hello World' in captured.out
        assert '1 Goodbye World' in captured.out

    def test_grep_flag_i(self, capsys):
        grep({'i'}, ['heLLo', 'file1.txt'])
        captured = capsys.readouterr()
        
        assert '1 Hello World' in captured.out

    def test_grep_flag_i_long(self, capsys):
        grep({'ignore-case'}, ['heLLo', 'file1.txt'])
        captured = capsys.readouterr()
        
        assert '1 Hello World' in captured.out

    def test_grep_r(self, capsys):
        grep({'r'}, ['Hello', self.test_dir])
        captured = capsys.readouterr()
        
        assert '1 Hello World' in captured.out
        assert '1 Hello from subdir' in captured.out

    def test_grep_r_long(self, capsys):
        grep({'recursive'}, ['Hello', self.test_dir])
        captured = capsys.readouterr()
        
        assert '1 Hello World' in captured.out
        assert '1 Hello from subdir' in captured.out

    def test_grep_flag_r_i(self, capsys):
        grep({'r', 'i'}, ['heLLo', self.test_dir])
        captured = capsys.readouterr()
        
        assert '1 Hello World' in captured.out
        assert '1 Hello from subdir' in captured.out

    def test_grep_regex(self, capsys):
        grep(set(), [r'P\w+', 'file1.txt'])
        captured = capsys.readouterr()
        
        assert 'Python' in captured.out

    def test_grep_no_match(self, capsys):
        grep(set(), ['NotFound', 'file1.txt'])
        captured = capsys.readouterr()
        
        assert not captured.out

    def test_grep_incorrect_flag(self):
        with pytest.raises(src.config.exceptions.IncorrectFlag):
            grep({'a'}, ['pattern', 'file1.txt'])

    def test_grep_nonexistent_file(self):
        with pytest.raises(src.config.exceptions.PathError):
            grep(set(), ['pattern', 'haha.txt'])

    def test_grep_empty_pattern(self, capsys):
        grep(set(), ['', 'file1.txt'])
        captured = capsys.readouterr()
        
        assert not captured.out

    def test_grep_special_regex(self, capsys):
        test_file = Path(self.test_dir, 'special.txt')
        test_file.write_text('Price: $100\nEmail: test@example.com\n')
        grep(set(), [r'\$\d+|\@+', 'special.txt'])
        captured = capsys.readouterr()
        
        assert '1 Price: $100' in captured.out
        assert '2 Email: test@example.com' in captured.out

    def test_grep_non_regex(self, capsys):
        file = Path(self.test_dir, 'test.txt')
        file.write_text('Hello [World]\nTest\n')
        
        grep(set(), ['[', 'test.txt'])
        captured = capsys.readouterr()
        
        assert '1 Hello [World]' in captured.out

    def test_grep_non_regex_flag_i(self, capsys):
        file = Path(self.test_dir, 'test.txt')
        file.write_text('Hello [World]\nTest\n')
        
        grep({'i'}, ['[worLD', 'test.txt'])
        captured = capsys.readouterr()
        
        assert '1 hello [world]' in captured.out

    def test_grep_permission_error(self, capsys):
        file = Path(self.test_dir, 'test.txt')
        file.write_text('Secret content')
        original_mode = file.stat().st_mode
        try:
            file.chmod(0o000)
            grep(set(), ['Secret', 'test.txt'])
            captured = capsys.readouterr()
            
            assert 'Нет прав на чтение' in captured.out
        finally:
            file.chmod(original_mode)

    def test_grep_binary_file(self, capsys):
        bin_file = Path(self.test_dir, 'binary.bin')
        bin_file.write_bytes(b'\xff\xfe\xfd\xfc')
        grep(set(), ['pattern', 'binary.bin'])
        captured = capsys.readouterr()
        
        assert 'невозможно прочитать' in captured.out

    def test_grep_complex_regex(self, capsys):
        email_file = Path(self.test_dir, 'emails.txt')
        email_file.write_text('Contact: user@example.com\nInvalid: not an email\n')
        grep(set(), [r'\w+@\w+\.\w+', 'emails.txt'])
        captured = capsys.readouterr()
        
        assert 'user@example.com' in captured.out
        assert 'not an email' not in captured.out

    def test_grep_recursive_nested_dirs(self, capsys):
        deep = Path(self.test_dir, 'subdir', 'nested')
        deep.mkdir()
        Path(deep, 'deep.txt').write_text('Deep content\n')
        
        grep({'r'}, ['Deep', self.test_dir])
        captured = capsys.readouterr()
        
        assert 'Deep content' in captured.out

    def test_grep_first_arg_is_file(self, capsys):
        grep(set(), ['file1.txt'])
        captured = capsys.readouterr()
        
        assert not captured.out
        