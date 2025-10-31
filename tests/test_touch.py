import os
import shutil
import tempfile
from pathlib import Path

import pytest

import src.config.exceptions
from src.utilities.touch import touch


class TestTouchCommand:

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

        Path(self.test_dir, 'existing.txt').write_text('Exist')

        yield

        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_touch_file(self):
        touch(set(), ['newfile.txt'])

        assert Path(self.test_dir, 'newfile.txt').exists()

    def test_touch_files(self):
        touch(set(), ['file1.txt', 'file2.txt', 'file3.txt'])

        assert Path(self.test_dir, 'file1.txt').exists()
        assert Path(self.test_dir, 'file2.txt').exists()
        assert Path(self.test_dir, 'file3.txt').exists()

    def test_touch_with_relative_path(self):
        touch(set(), ['./newfile.txt'])

        assert Path(self.test_dir, 'newfile.txt').exists()

    def test_touch_with_abs_path(self):
        abs_path = os.path.join(self.test_dir, 'abs.txt')
        touch(set(), [abs_path])
        assert Path(abs_path).exists()

    def test_touch_existing_file(self, capsys):
        touch(set(), ['existing.txt'])
        captured = capsys.readouterr()

        assert 'existing.txt пропущен: уже существует' in captured.out
        assert Path(self.test_dir, 'existing.txt').read_text() == 'Exist'

    def test_touch_partitial_success(self, capsys):
        touch(set(), ['file1.txt', 'existing.txt', 'file2.txt'])
        captured = capsys.readouterr()
        
        assert 'existing.txt пропущен: уже существует' in captured.out
        assert Path(self.test_dir, 'file1.txt').exists()
        assert Path(self.test_dir, 'file2.txt').exists()

    def test_touch_in_subdir(self):
        subdir = Path(self.test_dir, 'subdir')
        subdir.mkdir()
        touch(set(), ['subdir/newfile.txt'])

        assert Path(self.test_dir, 'subdir', 'newfile.txt').exists()

    def test_touch_with_flag(self):
        with pytest.raises(src.config.exceptions.IncorrectFlag):
            touch({'a'}, ['file.txt'])

    def test_touch_with_flags(self):
        with pytest.raises(src.config.exceptions.IncorrectFlag):
            touch({'a', 'b'}, ['file.txt'])

    def test_touch_file_with_special_chars(self):
        touch(set(), ['file_12 3-test.txt'])
        assert Path(self.test_dir, 'file_12 3-test.txt').exists()

    def test_touch_hidden_file(self):
        touch(set(), ['.hidden'])

        assert Path(self.test_dir, '.hidden').exists()

    def test_touch_many_files(self):
        files = [f'file_{i}.txt' for i in range(50)]
        touch(set(), files)

        assert all(Path(self.test_dir, file).exists() for file in files)

    def test_touch_with_parent_notation(self):
        subdir = Path(self.test_dir, 'subdir')
        subdir.mkdir()
        os.chdir(subdir)
        
        touch(set(), ['../file1.txt'])
        assert Path(self.test_dir, 'file1.txt').exists()

    def test_touch_nonexist_dir(self):
        with pytest.raises(src.config.exceptions.PathError):
            touch(set(), ['nonexist_dir/file.txt'])

    def test_touch_file_different_extensions(self):
        touch(set(), ['file.txt', 'file.py', 'file.md', 'file.json'])

        assert Path(self.test_dir, 'file.txt').exists()
        assert Path(self.test_dir, 'file.py').exists()
        assert Path(self.test_dir, 'file.md').exists()
        assert Path(self.test_dir, 'file.json').exists()

    def test_touch_file_no_extension(self):
        touch(set(), ['README'])

        assert Path(self.test_dir, 'README').exists()

    def test_touch_is_empty_file(self):
        touch(set(), ['empty.txt'])
        file_path = Path(self.test_dir, 'empty.txt')

        assert file_path.exists()
        assert not file_path.read_text()

    def test_touch_with_tilde(self):
        home = os.path.expanduser('~')
        test = os.path.join(home, 'tilde_test')
        try:
            touch(set(), [test])
            assert Path(test).exists()
        finally:
            if os.path.exists(test):
                os.remove(test)
    
    def test_touch_permission_error(self, capsys):
        dir = Path(self.test_dir, 'dir')
        dir.mkdir()
        original_modes = dir.stat().st_mode
        dir.chmod(0o000)
        try:
            touch({}, ['dir/test.txt'])
            captured = capsys.readouterr()

            assert 'Нет прав на создание dir/test.txt' in captured.out
        finally:
            dir.chmod(original_modes)
            shutil.rmtree(dir)
