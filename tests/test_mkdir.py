import os
import shutil
import tempfile
from pathlib import Path

import pytest

import src.config.exceptions
from src.utilities.mkdir import mkdir


class TestMkdirCommand:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

        Path(self.test_dir, 'exist_dir').mkdir()

        yield

        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_mkdir_dir(self):
        mkdir(set(), ['newdir'])

        assert Path(self.test_dir, 'newdir').exists()
        assert Path(self.test_dir, 'newdir').is_dir()

    def test_mkdir_dirs(self):
        mkdir(set(), ['dir1', 'dir2', 'dir3'])

        assert Path(self.test_dir, 'dir1').exists()
        assert Path(self.test_dir, 'dir1').is_dir()
        assert Path(self.test_dir, 'dir2').exists()
        assert Path(self.test_dir, 'dir2').is_dir()
        assert Path(self.test_dir, 'dir3').exists()
        assert Path(self.test_dir, 'dir3').is_dir()

    def test_mkdir_with_relative_path(self):
        mkdir(set(), ['./newdir'])

        assert Path(self.test_dir, 'newdir').exists()
        assert Path(self.test_dir, 'newdir').is_dir()

    def test_mkdir_with_abs_path(self):
        abs_path = os.path.join(self.test_dir, 'abs_dir')
        mkdir(set(), [abs_path])

        assert Path(abs_path).exists()
        assert Path(abs_path).is_dir()

    def test_mkdir_exist_dir(self, capsys):
        mkdir(set(), ['exist_dir'])
        captured = capsys.readouterr()

        assert 'exist_dir пропущен: уже существует' in captured.out

    def test_mkdir_partial_success(self, capsys):
        mkdir(set(), ['dir1', 'exist_dir', 'dir2'])
        captured = capsys.readouterr()

        assert 'exist_dir пропущен: уже существует' in captured.out
        assert Path(self.test_dir, 'dir1').exists()
        assert Path(self.test_dir, 'dir1').is_dir()
        assert Path(self.test_dir, 'dir2').exists()
        assert Path(self.test_dir, 'dir2').is_dir()

    def test_mkdir_in_subdir(self):
        subdir = Path(self.test_dir, 'subdir')
        subdir.mkdir()
        mkdir(set(), ['subdir/newdir'])

        assert Path(self.test_dir, 'subdir', 'newdir').exists()
        assert Path(self.test_dir, 'subdir', 'newdir').is_dir()

    def test_mkdir_incorrect_path(self, capsys):
        mkdir(set(), ['haha/newdir'])
        captured = capsys.readouterr()

        assert 'haha/newdir пропущен' in captured.out

    def test_mkdir_partial_success2(self, capsys):
        mkdir(set(), ['dir1', 'haha/dir2', 'dir3'])
        captured = capsys.readouterr()

        assert 'haha/dir2 пропущен' in captured.out
        assert Path(self.test_dir, 'dir1').exists()
        assert Path(self.test_dir, 'dir1').is_dir()
        assert Path(self.test_dir, 'dir3').exists()
        assert Path(self.test_dir, 'dir3').is_dir()

    def test_mkdir_with_flag(self):
        with pytest.raises(src.config.exceptions.IncorrectFlag):
            mkdir({'a'}, ['newdir'])

    def test_mkdir_with_special_chars(self):
        mkdir(set(), ['dir_123-te st'])

        assert Path(self.test_dir, 'dir_123-te st').exists()

    def test_mkdir_many_dirs(self):
        dirs = [f'dir_{i}' for i in range(50)]
        mkdir(set(), dirs)

        assert all(Path(self.test_dir, dirname).exists() for dirname in dirs)

    def test_mkdir_with_parent_path(self):
        subdir = Path(self.test_dir, 'subdir')
        subdir.mkdir()
        os.chdir(subdir)
        mkdir(set(), ['../parent_dir'])

        assert Path(self.test_dir, 'parent_dir').exists()

    def test_mkdir_numeric_name(self):
        mkdir(set(), ['123', '456'])

        assert Path(self.test_dir, '123').exists()
        assert Path(self.test_dir, '123').is_dir()
        assert Path(self.test_dir, '456').exists()
        assert Path(self.test_dir, '456').is_dir()

    def test_mkdir_existing_file_same_name(self, capsys):
        Path(self.test_dir, 'filename').touch()
        mkdir(set(), ['filename'])
        captured = capsys.readouterr()

        assert 'filename пропущен: уже существует' in captured.out

    def test_mkdir_slash(self):
        mkdir(set(), ['newdir/'])

        assert Path(self.test_dir, 'newdir').exists()

    def test_mkdir_mixed_errors(self, capsys):
        Path(self.test_dir, 'exists').mkdir()
        mkdir(set(), ['exists', 'haha/test', 'success'])
        captured = capsys.readouterr()

        assert 'exists пропущен: уже существует' in captured.out
        assert 'haha/test пропущен' in captured.out
        assert Path(self.test_dir, 'success').exists()
